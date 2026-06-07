from .batch_llm_wrapper import BatchLLMWrapper
import json
import os
import mimetypes

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

from .utils import read_json


class BatchClaudeWrapper(BatchLLMWrapper):
    """
    Anthropic batch wrapper with optional structured output.

    Pass ``structured_output=<tool_dict>`` to force Claude to return JSON
    via tool use instead of free text.  The tool dict must have the shape:

        {
            "name": "...",
            "description": "...",
            "input_schema": { ... }   # JSON-Schema object
        }

    Build it with ``lapa_schema.build_extraction_tool()`` or supply your own.
    When ``structured_output`` is not provided the wrapper behaves exactly as
    before (plain-text response).

    Example
    -------
    from lapa_schema import build_extraction_tool

    model = BatchClaudeWrapper(
        api_key        = read_txt(args.api_key),
        max_tokens     = args.max_tokens,
        model          = args.model,
        system_prompt  = system_prompt,
        structured_output = build_extraction_tool(),   # <— opt-in
    )
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.api_key       = kwargs.get("api_key", "")
        self.model         = kwargs.get("model", "claude-sonnet-4-6")
        self.name          = f"claude_{self.model}"
        self.max_tokens    = kwargs.get("max_tokens", 16000)
        self.media_type    = kwargs.get("media_type", "image/jpg")
        self.system_prompt = kwargs.get("system_prompt", None)

        # Optional: a tool definition dict that forces structured JSON output.
        # None  → behave as before (free-text response).
        # dict  → use tool_choice to guarantee the model calls this tool.
        self.structured_output: dict | None = kwargs.get("structured_output", None)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_system(self) -> list[dict] | None:
        """Return the system prompt block (with prompt-caching header) or None."""
        if not self.system_prompt:
            return None
        return [
            {
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ]

    def _build_messages(self, prompt) -> list[dict]:
        """Build the messages array for a single prompt."""
        content = [{"type": "text", "text": prompt.content}]

        if len(prompt.images) > 0:
            mime, _ = mimetypes.guess_type(prompt.images[0])
            if mime not in {"image/jpeg", "image/png", "image/gif", "image/webp"}:
                mime = self.media_type
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime,
                        "data": prompt.get_image_array()[0],
                    },
                }
            )

        return [{"role": "user", "content": content}]

    def _extra_params(self) -> dict:
        """
        Return extra kwargs for MessageCreateParamsNonStreaming.

        When structured_output is set, adds ``tools`` and ``tool_choice``
        so Claude is forced to call the extraction tool.
        """
        if self.structured_output is None:
            return {}
        return {
            "tools": [self.structured_output],
            "tool_choice": {
                "type": "tool",
                "name": self.structured_output["name"],
            },
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit_tasks(self, prompts):
        super().submit_tasks()

        prompts_and_ids = []
        requests        = []
        system          = self._build_system()
        extra           = self._extra_params()

        for prompt in prompts:
            request_id = self.get_request_id()
            prompts_and_ids.append({"id": request_id, "prompt": prompt})

            params = MessageCreateParamsNonStreaming(
                model      = self.model,
                max_tokens = self.max_tokens,
                messages   = self._build_messages(prompt),
                **({"system": system} if system else {}),
                **extra,
            )

            requests.append(
                Request(custom_id=request_id, params=params)
            )

        client         = anthropic.Anthropic(api_key=self.api_key)
        message_batch  = client.messages.batches.create(requests=requests)

        return self._process_end(
            json.loads(message_batch.to_json()), prompts_and_ids
        )

    def poll(self, request_output_path):
        client     = anthropic.Anthropic(api_key=self.api_key)
        request_id = read_json(request_output_path)["content"]["id"]
        batch      = client.messages.batches.retrieve(request_id)
        return json.loads(batch.to_json())

    def retrieve_tasks(self, request_output_path):
        client     = anthropic.Anthropic(api_key=self.api_key)
        request_id = read_json(request_output_path)["content"]["id"]

        results = {}

        for result in client.messages.batches.results(request_id):
            match result.result.type:

                case "succeeded":
                    content_blocks = result.result.message.content

                    if self.structured_output is not None:
                        # ── Structured mode: extract the tool_use block ──────────
                        tool_block = next(
                            (b for b in content_blocks if b.type == "tool_use"),
                            None,
                        )
                        if tool_block:
                            # .input is already a parsed dict — no json.loads needed
                            results[result.custom_id] = tool_block.input
                        else:
                            # Unexpected: tool call absent — fall back to raw text
                            text_block = next(
                                (b for b in content_blocks if b.type == "text"),
                                None,
                            )
                            results[result.custom_id] = {
                                "content": text_block.text if text_block else str(result),
                                "type": "missing_tool_call",
                            }
                    else:
                        # ── Plain-text mode: original behaviour ──────────────────
                        results[result.custom_id] = (
                            result.result.message.content[0].text
                        )

                case "errored":
                    error_type = (
                        "invalid_request"
                        if result.result.error.type == "invalid_request"
                        else "server_error"
                    )
                    results[result.custom_id] = {
                        "content": str(result),
                        "type": error_type,
                    }

                case "expired":
                    results[result.custom_id] = {
                        "content": str(result),
                        "type": "expired_error",
                    }

        return self._end_retrieve(results)
