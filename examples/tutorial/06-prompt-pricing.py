import llmwrap
import os

# Create prompt:
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "example_prompt.txt")
prompt = llmwrap.Prompt(prompt_source, options = {"name" : "Jacob", "question" : "How are you?"})

# image_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "moleman.jpeg")
# prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "describe.txt")
# prompt = llmwrap.Prompt(prompt_source, images = [image_source])

openai_wrapper = llmwrap.OpenAIWrapper("gpt-4o")
pricing = openai_wrapper.token_process(prompt, 1500)

for item in pricing:
    print(f"{item}: {pricing[item]}")