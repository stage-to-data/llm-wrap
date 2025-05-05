from .batch_response import BatchResponse, BatchResponseContent
import time
import uuid

class BatchLLMWrapper:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.process_started = None
        self.process_ended = None
        self.process_time = None

    def submit_tasks(self):
        self.process_started = time.perf_counter()

    def _process_end(self, content, prompts):
        self.process_ended = time.perf_counter()
        self.process_time = self.process_ended - self.process_started

        return BatchResponse(content, prompts, self)
    
    def get_request_id(self):
        return str(uuid.uuid4())
    
    def _end_retrieve(self, results_dict):
        full_result_dict = {}
        for key in results_dict:
            full_result_dict[key] = BatchResponseContent(results_dict[key], self, key)
        return full_result_dict