from .llm_wrapper import LLMWrapper
from anthropic import Anthropic
import tiktoken
import base64
import json
import os

class ClaudeImageExtractor:
    def __init__(self, api_key=None):

        self.api_key = kwargs.get("api_key_claude", "")    
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-7-sonnet-20250219"  # Using Claude 3.7 Sonnet


    def encode_image(self, image_path):
        """Convert an image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    
    def extract_text_from_image(self, image_path, prompt_template=None):
        """Extract text from an image using Claude API."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Default prompt for text extraction
        if prompt_template is None:
            prompt_template = """
            Please extract all the text you see in this theater program image.
            Organize it by sections, maintaining the original structure as much as possible.
            Include titles, cast lists, show descriptions, dates, and any other textual information.    Do not change or modify the information in any way.
            Make sure all the text is extracted.
            Format the information clearly in markdown, maintaining the hierarchical structure.
            """
        
        # Encode the image
        base64_image = self.encode_image(image_path)
        
        # Create message with image
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_template
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        )
        
        # Extract the response text
        return message.content[0].text    



if __name__ == "__main__":

    extractor = ClaudeImageExtractor()
    
    # Example 1: Extract text from a single image
    result = extractor.extract_text_from_image("/Users/antonioslagarias/Downloads/programme-off13-29_page-0001.jpg")
    print(result)