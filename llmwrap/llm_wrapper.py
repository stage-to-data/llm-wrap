from .response import Response
import time


class LLMWrapper:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.process_started = None
        self.process_ended = None
        self.process_time = None

    def process(self):
        self.process_started = time.perf_counter()

    def _process_end(self, content, prompt):
        self.process_ended = time.perf_counter()
        self.process_time = self.process_ended - self.process_started

        return Response(content, prompt, self)
