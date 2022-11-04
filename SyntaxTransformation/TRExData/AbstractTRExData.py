from typing import Dict, List, Tuple, Callable

from .LamaTRExData import LamaTRExData


def is_abstract(labels: Tuple[str, str]) -> bool:
    subj, obj = labels
    return obj.islower() and subj.islower()


class AbstractTRExData(LamaTRExData):
    def __init__(self, train: bool = False, relations=None):
        super().__init__(train, relations)

    def load(self):
        super().load()
        self.filter_data(is_abstract)
