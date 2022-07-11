from typing import Dict, Callable, List, Tuple

from tqdm import tqdm
import torch.nn as nn

from relation_templates.templates import get_template_list, get_templates
from SentenceTypologyQueryResults import SentenceTypologyQueryResults

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"

KEYS = [SIMPLE, COMPOUND, COMPLEX, COMCOM]


class TypologyQuerier:
    def __init__(self, model: nn.Module, relations: List[str], top_k: int, mask_token: str , keys: List = KEYS):
        self.model: nn.Module = model
        self.relations: List[str] = relations
        self.keys: List[str] = keys
        self.top_k: int = top_k
        self.results: SentenceTypologyQueryResults = SentenceTypologyQueryResults(self.relations, self.top_k, keys)
        self.queries: Dict[str, List[Tuple[str, str, str]]] = {relation: [] for relation in self.relations}
        self.mask: str = mask_token

    def query(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation]):
                templates: Dict = get_templates(relation, sub, self.mask, self.keys)
                answers: Dict[str, List] = {key:self.model(templates[key]) for key in self.keys}
                self.results.process_answers(obj, relation, answers)

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        self.results.set_top_k(top_k)

    def set_model(self, model: nn.Module):
        self.model: nn.Module = model

    def reset(self):
        self.results = SentenceTypologyQueryResults(self.relations, self.top_k, self.keys)

    def print_result(self):
        self.results.print_result()

    def print_global_result(self):
        self.results.print_global_result()

    def print_for_latex(self, header_kex: str = "accuracy"):
        for row in self.results.print_for_latex(header_kex):
            print(row)
