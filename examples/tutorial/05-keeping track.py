import llmwrap
import os

# Set an output destination:
output_dest = os.path.join(os.getcwd(), "examples", "tutorial", "output")

# Get prompt:
prompot_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "example_prompt.txt")
prompt = llmwrap.Prompt(prompot_source, options = {"name" : "Jacob", "question" : "How are you?"})

# Get some LLM wrappers:
llms = [
    llmwrap.OllamaWrapper("deepseek-r1:7b"),
    llmwrap.OllamaWrapper("llama3.2:1b")
]

# Get the answers:
for llm in llms:
    print(f"Treating: {llm.name}...")

    response = llm.process(prompt)
    
    print(f"--> Finished in {response.process_time} ms")

    response.write(output_dest)