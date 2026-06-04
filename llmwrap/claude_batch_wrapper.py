from .batch_llm_wrapper import BatchLLMWrapper
import tiktoken
import base64
import json
import os
from .utils import read_json
import mimetypes

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

class BatchClaudeWrapper(BatchLLMWrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.api_key = kwargs.get("api_key", "")
        self.model = kwargs.get("model", "claude-sonnet-4-6")
        # self.client = Anthropic(api_key=self.api_key)
        self.name = f"claude_{self.model}"
        self.max_tokens = kwargs.get("max_tokens", 16000)
        self.media_type = kwargs.get("media_type", "image/jpg")
        self.system_prompt = kwargs.get("system_prompt", None)

    def submit_tasks(self, prompts):
        super().submit_tasks()

        prompts_and_ids = []
        requests = []

        for prompt in prompts:
            request_id = self.get_request_id()
            prompts_and_ids.append({"id" : request_id, "prompt" : prompt})

            messages = [{
                "role": "user",
                "content" : [{"type": "text", "text": prompt.content}]
            }]

            if len(prompt.images) > 0:
                mime, encoding = mimetypes.guess_type(prompt.images[0])
                if mime not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                    mime = self.media_type

                messages[0]["content"].append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime,
                        "data": prompt.get_image_array()[0]
                    }
                })

            system = None
            if self.system_prompt:
                system = [
                    {
                        "type": "text",
                        "text": self.system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ]
            
            requests.append(Request(
                custom_id = request_id,
                params = MessageCreateParamsNonStreaming(
                    model = self.model,
                    max_tokens = self.max_tokens,
                    messages = messages,
                    **({"system": system} if system else {}) 
                )
            ))
        
        client = anthropic.Anthropic(api_key = self.api_key)
        message_batch = client.messages.batches.create(requests = requests)

        return self._process_end(json.loads(message_batch.to_json()), prompts_and_ids)

    def poll(self, request_output_path):
        client = anthropic.Anthropic(api_key = self.api_key)

        request_id = read_json(request_output_path)["content"]["id"]

        message_batch = client.messages.batches.retrieve(request_id)
        return json.loads(message_batch.to_json())
    
    def retrieve_tasks(self, request_output_path):
        client = anthropic.Anthropic(api_key = self.api_key)

        request_id = read_json(request_output_path)["content"]["id"]

        results = {}

        for result in client.messages.batches.results(request_id):
            match result.result.type:
                case "succeeded":
                    results[result.custom_id] = result.result.message.content[0].text
                case "errored":
                    if result.result.error.type == "invalid_request":
                        results[result.custom_id] = {"content": str(result), "type" : "validation_error"}
                    else:
                        results[result.custom_id] = {"content": str(result), "type" : "server_error"}
                case "expired":
                    results[result.custom_id] = {"content": str(result), "type" : "expired_error"}

        return self._end_retrieve(results)