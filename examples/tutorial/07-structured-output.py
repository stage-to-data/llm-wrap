# To create structured output in python, you can use pydantic's BaseModel class.
# First, import the class
from pydantic import BaseModel

# Then create some subclasses of BoseModel to structure your output:
class FriendInfo(BaseModel):
  name: str
  age: int
  is_available: bool

class FriendList(BaseModel):
  friends: list[FriendInfo]

# BaseModel has a function called model_json_schema() that formats the
# structure to json, this gives you an idea about what some of the models will use:
print(FriendList.model_json_schema())

# Now we can create our prompt:
import llmwrap
prompt = llmwrap.Prompt(
  "I have two friends. The first is Ollama 22 years old busy saving the world, and the second is Alonso 23 years old and wants to hang out. Return a list of friends in JSON format",
  output_structure = FriendList
)

# Now let's run the process:
llm = llmwrap.OllamaWrapper("gpt-oss:20b")
response = llm.process(prompt)
print(response.content)

# import os
# from utils import read_txt
# api_key = read_txt(os.path.join(os.getcwd(), "examples", "tutorial", "assets", "openai_key.txt"))
# llm = llmwrap.OpenAIWrapper("gpt-4o", api_key = api_key)
# response = llm.process(prompt)
# print(response.content)

# Finally, you can verify the validity of the returned content:
friends_response = FriendList.model_validate_json(response.content)
print(friends_response)