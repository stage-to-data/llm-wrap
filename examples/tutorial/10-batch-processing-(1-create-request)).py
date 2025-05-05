import llmwrap
import os
from utils import read_txt, collect_files

# Output destination
output_dest = os.path.join(os.getcwd(), "examples", "tutorial", "output")

# Claude API key:
api_key = read_txt(os.path.join(os.getcwd(), "examples", "tutorial", "assets", "claude_key.txt"))

# Get prompt and image sources:
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "describe.txt")
image_sources = collect_files(os.path.join(os.getcwd(), "examples", "tutorial", "assets"), ["jpeg", "jpg"])

# Create a list of prompts:
prompts = []
for image_path in image_sources:
    prompts.append(llmwrap.Prompt(prompt_source, images = [image_path]))
print(f"Create a list of {len(prompts)} prompts.")

# Create an instance of a batch LLM wrapper:
multimodal_model = llmwrap.BatchClaudeWrapper(api_key = api_key)

# Submit the tasks to the LLM:
response = multimodal_model.submit_tasks(prompts)

# Save the results so that you can poll the request later
path = response.write(output_dest)
print(path)