import llmwrap

model_name = "qwen3-embedding:8b"

model = llmwrap.OllamaWrapper(model_name)

embedding = model.embed("Hello world")

print(embedding)
print(type(embedding))