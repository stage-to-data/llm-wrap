from .llm_wrapper import LLMWrapper
import openai
import tiktoken

class OpenAIWrapper(LLMWrapper):

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.name = f"openai_{model}"
        self.model = model
        self.options = kwargs.get("options", {})
        self.api_key = kwargs.get("api_key", "")
        self.system_prompt = kwargs.get("system_prompt", "Please answer my questions as precisely and concisely as possible.")
        self.max_tokens = kwargs.get("max_tokens", 1500)

        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=openai.api_key)

        # Example pricing per 1,000 tokens in USD (update as per OpenAI's latest pricing)
        self.model_pricing = {
            "gpt-4o": {
                "input": 0.005,  # $0.005 per 1K tokens (input)
                "output": 0.015  # $0.015 per 1K tokens (output)
            },
            "gpt-4-turbo": {
                "input": 0.01,
                "output": 0.03
            },
            "gpt-3.5-turbo": {
                "input": 0.001,
                "output": 0.002
            }
        }
        self.image_pricing = {
            "default": 0.01  # $0.01 per image (adjust according to image resolution if needed)
        }

    def _process_prompt(self, prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": [{"type": "text", "text": str(prompt.content)}]}
        ]

        if len(prompt.images) > 0:
            messages[1]['content'].append({
                "type" : "image_url", "image_url" : {"url" : f"data:image/png;base64,{prompt.get_image_array()[0]}"}
            })
        
        return messages

    def token_process(self, prompt, output_tokens_estimate = 500):
        messages = self._process_prompt(prompt)

        num_tokens = self._count_tokens(messages)

        return self._estimate_cost(num_tokens, len(prompt.images), output_tokens_estimate)

    def process(self, prompt):
        super().process()
        
        messages = self._process_prompt(prompt)

        if prompt.output_structure == None:
            try:
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages = messages,
                    max_tokens = self.max_tokens
                )
            except Exception as e:
                print(e)
                return None
        else:
            try:
                response = self.client.beta.chat.completions.parse(
                    model = self.model,
                    messages = messages,
                    max_tokens = self.max_tokens,
                    response_format = prompt.output_structure 
                )
            except Exception as e:
                print(e)
                return None
        if response.choices:
            rep = super()._process_end(response.choices[0].message.content, prompt)
        else:
            rep = super()._process_end(None, prompt)

        return rep
 
    def _count_tokens(self, messages):
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Default encoding if model not found (you can adjust this default)
            encoding = tiktoken.get_encoding("cl100k_base")
        
        total_tokens = 0
        
        for message in messages:
            # Count role
            role_tokens = encoding.encode(message["role"])
            total_tokens += len(role_tokens) + 4  # Accounting for formatting tokens

            # Check content type
            content = message.get("content", "")

            if isinstance(content, str):
                # Plain text
                total_tokens += len(encoding.encode(content))
            
            elif isinstance(content, list):
                # Likely multimodal
                for item in content:
                    if item["type"] == "text":
                        total_tokens += len(encoding.encode(item["text"]))
                    elif item["type"] == "image_url":
                        pass  # Images are billed separately, not via tokens
        return total_tokens
    
    def _estimate_cost(self, input_tokens, num_images, output_tokens_estimate):
        if self.model not in self.model_pricing:
            raise ValueError(f"Model '{self.model}' not found in MODEL_PRICING. Add pricing data.")

        input_price = (input_tokens / 1000) * self.model_pricing[self.model]["input"]
        output_price = (output_tokens_estimate / 1000) * self.model_pricing[self.model]["output"]

        # Handle image cost if images are included
        image_price = num_images * self.image_pricing.get("default", 0)

        total_price = input_price + output_price + image_price

        return {
            "model": self.model,
            "input_tokens": input_tokens,
            "output_tokens_estimate": output_tokens_estimate,
            "input_price_usd": round(input_price, 6),
            "output_price_usd": round(output_price, 6),
            "image_price_usd": round(image_price, 6),
            "total_estimated_price_usd": round(total_price, 6)
        }