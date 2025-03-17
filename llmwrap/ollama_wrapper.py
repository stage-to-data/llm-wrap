from .llm_wrapper import LLMWrapper
from ollama import chat

class OllamaWrapper(LLMWrapper):

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.name = f"ollama_{model}"
        self.model = model
        self.options = kwargs.get("options", {})

    def process(self, prompt):
        super().process()

        messages = {'role': 'user', 'content': prompt.content}

        if len(prompt.images) > 0:
            messages['images'] = prompt.get_image_array()

        response = chat(
            model = self.model,
            messages = [messages],
            options = self.options
        )

        rep = super()._process_end(response.message.content, prompt)

        return rep