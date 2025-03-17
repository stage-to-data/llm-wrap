from .llm_wrapper import LLMWrapper
import openai

class OpenAIWrapper(LLMWrapper):

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.name = f"openai_{model}"
        self.model = model
        self.options = kwargs.get("options", {})
        self.api_key = kwargs.get("api_key", "")

        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=openai.api_key)


    def process(self, prompt):
        super().process()
        
        messages = [
        {"role": "system", "content": "You are an AI that extracts and organizes text from images."},
        {"role": "user", "content": [{"type": "text", "text": str(prompt.content)}]}
        ]

        if len(prompt.images) > 0:
            messages['content'].append({
                "type" : "image_url", "image_url" : {"url" : f"data:image/png;base64,{prompt.get_image_array()[0]}"}
            })


#       with open(image_path, "rb") as image_file:
#       base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        print(type(messages))
        print(type(messages[0])) 

        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            # options = self.options
            max_tokens = 1500
        )

        if response.choices:
            rep = super()._process_end(response.choices[0].message.content, prompt)
        else:
            rep = super()._process_end(None, prompt)

        return rep
 