from .llm_wrapper import LLMWrapper
from anthropic import Anthropic
import tiktoken
import base64
import json
import os
import mimetypes

class ClaudeWrapper(LLMWrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.api_key = kwargs.get("api_key", "")
        self.model = kwargs.get("model", "claude-3-7-sonnet-20250219")
        self.client = Anthropic(api_key=self.api_key)
        self.name = f"claude_{self.model}"
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.media_type = kwargs.get("media_type", "image/jpeg")

    def process(self, prompt):
        super().process()

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
        
        try:
            message = self.client.messages.create(
                model = self.model,
                max_tokens = self.max_tokens,
                messages = messages
            )
            rep = super()._process_end(message.content[0].text, prompt)
            return rep
        except Exception as e:
            return {"content": str(e), "type" : "error"}