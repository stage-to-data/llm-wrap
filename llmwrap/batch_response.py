import os
from .utils import write_json
from datetime import datetime
import uuid

class BatchResponse:
    def __init__(self, content, prompts, wrapper):
        self.content = content
        self.prompts = prompts
        self.wrapper = wrapper
        self.uuid = str(uuid.uuid4())

        self.process_time = self.wrapper.process_time

    def write(self, dest):
        if os.path.isdir(dest) is False:
            os.makedirs(dest)

        out = {
            "content": self.content,
            "process_time": self.process_time,
            "model": self.wrapper.name,
            "prompts": {},
            "uuid": self.uuid
        }

        for prompt in self.prompts:
            out[prompt] = self.prompts[prompt].content

        current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M")

        file_path = os.path.join(dest, f"{current_time_str}_{self.uuid}.json")
        write_json(file_path, out)

        return file_path
    
class BatchResponseContent:
    def __init__(self, content, wrapper, request_key):
        self.content = content
        self.wrapper = wrapper
        self.request_key = request_key
        self.uuid = str(uuid.uuid4())

        self.process_time = self.wrapper.process_time

    def write(self, dest):
        if os.path.isdir(dest) is False:
            os.makedirs(dest)

        out = {
            "content" : self.content,
            "model": self.wrapper.name,
            "uuid": self.uuid,
            "request_key" : self.request_key
        }

        current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M")

        file_path = os.path.join(dest, f"{current_time_str}_{self.uuid}.json")
        write_json(file_path, out)

        return file_path