import llmwrap
import os
from utils import read_txt

# Get prompt:
prompot_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "example_prompt.txt")
prompt=llmwrap.Prompt(prompot_source)

#image_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "moleman.jpeg")
#prompt = llmwrap.Prompt(prompot_source, images = [image_source])

#prompt = llmwrap.Prompt("How are you?")

# Get the LLM wrappers:
api_key = read_txt(os.path.join(os.getcwd(), "examples", "tutorial", "assets", "openai_key.txt"))
multimodal_model = llmwrap.OpenAIWrapper("gpt-4o")

# Get the response:
response = multimodal_model.process(prompt)
    
print(response.content)
print(f"--> Processing time: {response.process_time}")
