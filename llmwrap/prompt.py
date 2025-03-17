import os
from .utils import read_txt
import base64

class Prompt:
    def __init__(self, source, **kwargs):
        self.source = None
        self.options = kwargs.get("options", {})
        self.images = kwargs.get("images", [])

        if os.path.isfile(source):
            self.source = read_txt(source)
        else:
            self.source = source

        self.content = self._replace_source()

    def _replace_source(self):
        ret = self.source
        for key in self.options:
            ret = ret.replace(f"&&{key}", self.options[key])
        return ret
    
    def get_image_array(self):
        ret = []
        for img in self.images:
            with open(img, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            ret.append(base64_image)
        return ret