from typing import Dict, Callable, List, Tuple

from tqdm import tqdm
import torch.nn as nn

from relation_templates.P19_place_of_birth import retrieve_all_prompts as p19
from relation_templates.P36_capital import retrieve_all_prompts as p36
from relation_templates.P101_field_of_work import retrieve_all_prompts as p101
from relation_templates.P178_developer import retrieve_all_prompts as p178
from SentenceTypologyQueryResults import SentenceTypologyQueryResults

functions_for_relations: Dict[str, Callable[[str, str], List[str]]] = {
    "P19": p19,
    "P36": p36,
    "P101": p101,
    "P178": p178,
}


def templater(relation: str, sub: str, obj: str) -> List[str]:
    return functions_for_relations[relation](sub, obj)


def get_all_templates() -> List[str]:
    templates: List[str] = []
    for func in functions_for_relations.values():
        for template in func("subject", "object"):
            templates.append(template)
    return templates


class TypologyQuerier:
    def __init__(self, model: nn.Module, relations: List[str], top_k: int, mask_token: str):
        self.model: nn.Module = model
        self.relations: List[str] = relations
        self.top_k = top_k
        self.results: SentenceTypologyQueryResults = SentenceTypologyQueryResults(self.relations, self.top_k)
        self.queries: Dict[str, List[Tuple[str, str, str]]] = {relation: [] for relation in self.relations}
        self.mask: str = mask_token

    def query(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation]):
                query_simple, query_compound, query_complex, query_complex_compound = templater(relation, sub, self.mask)
                self.queries[relation].append((sub, obj, query_simple))
                res_simple = self.model(query_simple)
                res_compound = self.model(query_compound)
                res_complex = self.model(query_complex)
                res_complex_compound = self.model(query_complex_compound)
                self.results.process_answers(obj, relation,
                                             [res_simple, res_compound, res_complex, res_complex_compound])

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        self.results.set_top_k(top_k)

    def set_model(self, model: nn.Module):
        self.model: nn.Module = model

    def reset(self):
        self.results = SentenceTypologyQueryResults(self.relations, self.top_k)

    def print_result(self):
        self.results.print_result()
