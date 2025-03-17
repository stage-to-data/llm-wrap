from setuptools import setup
from setuptools import find_packages

long_description= """
# llm wrap
"""

required = [
    "openai",
    "ollama",
    "tiktoken"
]

setup(
    name="llmwrap",
    version="0.0.1",
    description="",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/stage-to-data/llm-wrap",
    install_requires=required,
    packages=find_packages()
)