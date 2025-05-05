import os
from .utils import write_json
from datetime import datetime
import uuid

class Response:
    def __init__(self, content, prompt, wrapper):
        self.content = content
        self.prompt = prompt
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
            "prompt": self.prompt.content,
            "uuid": self.uuid
        }

        current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M")

        file_path = os.path.join(dest, f"{current_time_str}_{self.uuid}.json")
        write_json(file_path, out)

        return file_path