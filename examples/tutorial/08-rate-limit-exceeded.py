import llmwrap
import os
from utils import read_txt

# Openai API cannot surpass 30000 input tokens.

# Get prompt:
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "massive_prompt.txt")
prompt=llmwrap.Prompt(prompt_source)

# Get the LLM wrappers:
api_key = read_txt(os.path.join(os.getcwd(), "examples", "tutorial", "assets", "openai_key.txt"))
model = llmwrap.OpenAIWrapper("gpt-4o", api_key = api_key)

# Get the response:
response = model.process(prompt)

print(response)
print(response.content)