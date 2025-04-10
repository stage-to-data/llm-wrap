import llmwrap
import os
from utils import read_txt

# Get prompt:
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "example_prompt.txt")
prompt=llmwrap.Prompt(prompt_source, options = {"name" : "Jacob", "question" : "How are you?"})

image_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "moleman.jpeg")
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "describe.txt")
prompt = llmwrap.Prompt(prompt_source, images = [image_source])

# Get the LLM wrappers:
api_key = read_txt(os.path.join(os.getcwd(), "examples", "tutorial", "assets", "claude_key.txt"))
multimodal_model = llmwrap.ClaudeWrapper(api_key = api_key)

# Get the response:
response = multimodal_model.process(prompt)
    
print(response.content)
print(f"--> Processing time: {response.process_time}")