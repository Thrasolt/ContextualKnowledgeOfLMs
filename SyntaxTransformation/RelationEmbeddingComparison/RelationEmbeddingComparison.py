from typing import Callable, List, Dict, Tuple

import torch
from tqdm import tqdm

from .constants import KEYS, MASK, INPUT_ID_KEY



def create_initial_results(relations: List[str], keys: List[str]):
    return {
        relation: {keyName: (0.0, 0.0) for keyName in keys}
        for relation in relations}


def calculate_gram_matrix(embeddings: List[torch.Tensor]):
    embedding_matrix = torch.stack(embeddings)
    return torch.mm(embedding_matrix, embedding_matrix.T)


def build_row(relation: str, index:int, values: Dict[str, Tuple[float, float]]):
    row = [relation] + list(map(lambda vals: vals[index], values.values()))
    return row


class RelationEmbeddingComparison:
    def __init__(self, model: Callable, tokenizer: Callable,
                 #metric: Callable,
                 relations: List[str],
                 templater: Callable[[str, str, str, List[str]], Dict[str, str]], get_relation_meta: Callable,
                 #persist: Callable,
                 keys: List[str] = None, mask: str = MASK,
                 input_id_key: str = INPUT_ID_KEY, is_symmetric: bool = True):
        self.model: Callable = model
        self.tokenizer: Callable = tokenizer

        #self.metric: Callable = metric
        self.relations: List[str] = relations

        self.templater: Callable[[str, str, str, str], Dict[str, str]] = templater
        self.get_relation_meta: Callable[[str], str] = get_relation_meta

        self.keys: List[str] = keys
        self.mask: str = mask
        self.input_id_key: str = input_id_key
        self.is_symmetric: bool = is_symmetric

        if keys is None:
            self.keys = KEYS

        self.results: Dict[str, Dict[str, Tuple[float, float]]] = create_initial_results(relations, keys)

    def compare(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            print(relation, ":")

            relation_pocket = {key_name: [] for key_name in self.keys}

            for sub, obj in tqdm(triples[relation]):
                features: Dict[str, torch.Tensor] = self.get_features(relation, sub)
                for key_name in self.keys:
                    relation_pocket[key_name].append(features[key_name])

            for key_name in self.keys:
                gram_matrix = calculate_gram_matrix(relation_pocket[key_name])
                mean = torch.mean(gram_matrix)
                std =  torch.std(gram_matrix)
                self.results[relation][key_name] = (mean.item(), std.item())

    def get_features(self, relation: str, sub: str) -> Dict[str, torch.Tensor]:
        sentences: Dict[str, str] = self.templater(relation, sub, self.mask, self.keys)
        features: Dict[str, torch.Tensor] = {}
        for key in self.keys:
            sentence: str = sentences[key]
            single_feature: torch.Tensor = self.extract_mask_features(sentence)
            features[key] = single_feature
        return features
    def extract_mask_features(self, sentence: str) -> torch.Tensor:
        mask_id = self.tokenizer(f"{self.mask}")[self.input_id_key][1]
        index = self.tokenizer(sentence)[self.input_id_key].index(mask_id)
        return torch.tensor(self.model(sentence)[0][index])

    def print_rows(self):
        self.print_rows_for_index(0)
        self.print_rows_for_index(1)

    def print_rows_for_index(self, index: int):
        for relation, values in self.results.items():
            row = build_row(relation, index, values)
            print(",".join(map(lambda entry: str(entry), row)))
