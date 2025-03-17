import llmwrap
import os

# Give a txt file or string as source for a prompt, the &&key elements will be replaced.
prompt_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "example_prompt.txt")
prompt_source = "My name is &&name. &&question"

# Create an instance of the Prompt class with source and options.
prompt = llmwrap.Prompt(prompt_source, options = {"name" : "Jacob", "question" : "How are you?"})

# Gets automatically replaced on init:
print(prompt.content)