import llmwrap
import os

# Get prompt:
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "describe.txt")
image_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "moleman.jpeg")
prompt = llmwrap.Prompt(prompt_source, images = [image_source])

# Get the LLM wrappers:
multimodal_model = llmwrap.OllamaWrapper("llama3.2-vision:11b")

# Get the response:
response = multimodal_model.process(prompt)
    
print(response.content)
print(f"--> Processing time: {response.process_time}")