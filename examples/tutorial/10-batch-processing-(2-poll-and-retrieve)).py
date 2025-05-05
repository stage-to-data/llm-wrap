import llmwrap
import os
from utils import read_txt, collect_files

# Output destination
output_dest = os.path.join(os.getcwd(), "examples", "tutorial", "output")

# Request path:
request_path = "/Users/jacob/Documents/Repos/stage-to-data/llm-wrap/examples/tutorial/output/2025-05-05-14-12_8f59b80f-f94f-43ba-8c1b-0efd301309df.json"

# Output destination
output_dest = os.path.join(os.getcwd(), "examples", "tutorial", "output")

# Claude API key:
api_key = read_txt(os.path.join(os.getcwd(), "examples", "tutorial", "assets", "claude_key.txt"))

# Create an instance of a batch LLM wrapper:
multimodal_model = llmwrap.BatchClaudeWrapper(api_key = api_key)

# Get current status of job:
batch_poll = multimodal_model.poll(request_path)
print(f"Current status: {batch_poll['processing_status']}\n")

# Retrieve the results:
if batch_poll['processing_status'] == "ended":
    results_dict = multimodal_model.retrieve_tasks(request_path)

    for key in results_dict:
        print(f"Request key: {key}")
        print(f"Content: {results_dict[key].content}\n")

        # Write results to file:
        results_dict[key].write(output_dest)