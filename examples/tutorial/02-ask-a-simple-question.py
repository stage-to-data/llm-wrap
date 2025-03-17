import llmwrap
import os

# Get prompt:
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "example_prompt.txt")
prompt = llmwrap.Prompt(prompt_source, options = {"name" : "Jacob", "question" : "How are you?"})

# Get some LLM wrappers:
llms = [
    llmwrap.OllamaWrapper("deepseek-r1:7b"),
    llmwrap.OllamaWrapper("llama3.2:1b")
]

# Get the answers:
for llm in llms:
    print(f"\nLLM: {llm.name}:\nResponse:")

    response = llm.process(prompt)
    
    print(response.content)
    print(f"--> Processing time: {response.process_time}")
