from typing import Dict, List

from transformers import pipeline, Pipeline
import _pickle as pickle
from os.path import exists
from filelock import FileLock

CACHE_DIR = "/Users/tim/projects/ContextualKnowledgeOfLMs/pipe_cache"


def path_from_filename(filename: str) -> str:
    return f"{CACHE_DIR}/{filename}.pickle"


def save_to_pickle(filename: str, data: Dict):
    file_path: str = path_from_filename(filename)
    with FileLock(file_path):
        with open(file_path, 'wb') as handle:
            pickle.dump(data, handle)


def load_from_pickle(filename: str) -> Dict:
    with open(path_from_filename(filename), 'rb') as handle:
        return pickle.load(handle)


def check_for_cache(filename: str) -> bool:
    return exists(path_from_filename(filename))


class PipelineCacheWrapper:
    def __init__(self, task: str, model: str, top_k: int):
        self.model: str = model
        self.task: str = task
        self.top_k: int = top_k
        self.pipeline: Pipeline = pipeline(task, model=model, top_k=self.top_k)
        self.filename: str = f"{self.model}_{self.task}_{self.top_k}"
        self.cache: Dict = {}
        self.cache_updated: bool = False
        self.init_cache()

    def init_cache(self):
        if not check_for_cache(self.filename):
            save_to_pickle(self.filename, {})
        self.load_cache()

    def load_cache(self):
        self.cache = load_from_pickle(self.filename)

    def save_to_cache(self):
        if self.cache_updated:
            save_to_pickle(self.filename, self.cache)

    def __call__(self, sentence: str) -> List:
        if sentence in self.cache:
            return self.cache[sentence]
        answer: List = self.pipeline(sentence)
        self.cache[sentence] = answer
        self.cache_updated = True
        return answer







