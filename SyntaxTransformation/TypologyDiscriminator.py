from typing import Dict, Callable, List, Tuple, Union

from tqdm import tqdm
import torch.nn as nn

from TypologyQuerier import TypologyQuerier
from relation_templates.templates import get_relation_cardinality, get_templates, get_relation_name

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"

KEYS = [SIMPLE, COMPOUND, COMPLEX, COMCOM]


class TypologyDiscriminator(TypologyQuerier):
    def __init__(self, model: nn.Module, relations: List[str], top_k: int, mask_token: str, token: str, keys=None):
        if keys is None:
            keys = KEYS
        super().__init__(model, relations, top_k, mask_token, keys)
        self.token: str = token
        self.hard: Dict[str, List[Tuple[str, str]]] = {rel: [] for rel in self.relations}
        self.easy: Dict[str, List[Tuple[str, str]]] = {rel: [] for rel in self.relations}

    def discriminate(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation]):
                templates: Dict = get_templates(relation, self.token, self.mask, self.keys)
                answers: Dict[str, List] = {key: self.model(templates[key]) for key in self.keys}
                self.results.process_answers(obj, relation, answers)
                self.process_answer(sub, obj, relation, answers)

    def query_easy(self):
        self.reset()
        self.query(self.easy)

    def query_hard(self):
        self.reset()
        self.query(self.hard)

    def process_answer(self, sub: str, obj: str, relation: str, answers: Dict[str, List]):
        if self.is_easy(obj, answers):
            self.easy[relation].append((sub, obj))
        else:
            self.hard[relation].append((sub, obj))

    def is_easy(self, label: str, answers: Dict[str, List]):
        for key, answer in answers.items():
            for entry in answer[0:self.top_k]:
                token: str = entry["token_str"]
                if token == label:
                    return True
        return False

    def get_easy_count(self):
        return self.get_count(self.easy)

    def get_hard_count(self):
        return self.get_count(self.hard)

    def get_count(self, data: Dict[str, List[Tuple[str, str]]]) -> Tuple[Dict[str, int], List[str]]:
        rels = []
        res = {"total": 0}
        for relation in self.relations:
            count: int = len(data[relation])
            if count > 0:
                res["total"] += count
                res[relation] = count
                rels.append(relation)
        return res, rels

    def print_count_for_latex(self, category: str):
        data: Dict[str, List[Tuple[str, str]]] = self.easy if category == "easy" else self.hard
        break_down: Dict[str, int] = self.get_count(data)[0]
        rows: List[List[Union[str, int]]] = []
        for relation, count in break_down.items():
            if relation != "total":
                name: str = " - " if relation == "total" else get_relation_name(relation)
                cardinality: str = " - " if relation == "total" else get_relation_cardinality(relation)
                row: List[Union[str, int]] = [relation, name, cardinality, count]
                rows.append(row)

        rows = sorted(rows, key=lambda rw: f"{rw[2]}-{rw[0]}")
        rows = [["Total", " - ", " - ", break_down["total"]]] + rows
        for row in rows:
            print(f"{' & '.join(list(map(str, row))) } \\\\")
