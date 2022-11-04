from typing import Dict, List, Tuple, Callable

from .LamaTRExData import LamaTRExData


class HardTRExData(LamaTRExData):
    def __init__(self, get_filter: Callable[[str], Callable[[Tuple[str, str]], bool]], train: bool = False, relations=None):
        super().__init__(train, relations)
        self.get_filter: Callable[[str], Callable[[Tuple[str, str]], bool]] = get_filter

    def filter_data_with_relation(self, get_filter: Callable[[str], Callable[[Tuple[str, str]], bool]]):
        filtered_data: Dict[str, List[Tuple[str, str]]] = {}
        for rel, triples in self.data.items():
            filtered_triples: List[Tuple[str, str]] = list(filter(get_filter(rel), triples))
            if not len(filtered_triples) == 0:
                filtered_data[rel] = filtered_triples
        self.data = filtered_data

    def load(self):
        super().load()
        self.filter_data_with_relation(self.get_filter)


class HardKnownTRExData(HardTRExData):
    def __init__(self,
                 get_hard_filter: Callable[[str], Callable[[Tuple[str, str]], bool]],
                 get_known_filter: Callable[[str], Callable[[Tuple[str, str]], bool]],
                 train: bool = False, relations=None):
        super().__init__(get_hard_filter, train, relations)
        self.get_known_filter: Callable[[str], Callable[[Tuple[str, str]], bool]] = get_known_filter

    def load(self):
        super().load()
        self.filter_data_with_relation(self.get_known_filter)
