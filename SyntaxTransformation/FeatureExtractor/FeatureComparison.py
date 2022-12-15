from typing import Callable, List, Dict, Tuple

import torch
from tqdm import tqdm

from .constants import KEYS, CARDINALITIES, MASK, INPUT_ID_KEY


def create_initial_results(categories: List[str], keys: List[str]) -> Dict[str, Dict[str, List[float]]]:
    results = {}
    for cat in categories:
        results[cat] = {}
        key_pairs: List[Tuple[str, str]] = [(left, right) for left in keys for right in keys]
        for key_pair in key_pairs:
            results[cat][key_pair] = []
    return results


class FeatureComparison:
    def __init__(self, model: Callable, tokenizer: Callable,
                 metric: Callable, relations: List[str],
                 templater: Callable[[str, str, str], Dict[str, str]], get_relation_meta: Callable,
                 persist: Callable,
                 keys: List[str] = None, mask: str = MASK,
                 input_id_key: str = INPUT_ID_KEY, is_symmetric: bool = True):

        self.model: Callable = model
        self.tokenizer: Callable = tokenizer

        self.metric: Callable = metric
        self.relations: List[str] = relations

        self.templater: Callable[[str, str, str, str], Dict[str, str]] = templater
        self.get_relation_meta: Callable[[str], str] = get_relation_meta

        self.keys: List[str] = keys
        self.mask: str = mask
        self.input_id_key: str = input_id_key
        self.is_symmetric: bool = is_symmetric

        if keys is None:
            self.keys = KEYS

        self.persist: Callable = persist

        self.results: Dict = create_initial_results(self.relations, self.keys)
        key_pairs: List[Tuple[str, str]] = self.get_key_pairs()
        self.total_result: Dict[Tuple[str, str], List[float]] = {key_pair: [] for key_pair in key_pairs}
        self.cardinality_result: Dict = create_initial_results(CARDINALITIES, self.keys)

    def extract_mask_features(self, sentence: str) -> torch.Tensor:
        mask_id = self.tokenizer(f"{self.mask}")[self.input_id_key][1]
        index = self.tokenizer(sentence)[self.input_id_key].index(mask_id)
        return torch.tensor(self.model(sentence)[0][index])

    def get_cardinality(self, relation: str) -> str:
        return self.get_relation_meta(relation).split(" ")[-1]

    def compare(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            print(relation, ":")
            for sub, obj in tqdm(triples[relation]):
                features: Dict[str, torch.Tensor] = self.get_features(relation, sub)

                for left_key, right_key in self.get_key_pairs():
                    result = self.single_comparison(features, left_key, right_key, relation, sub, obj)
                    card = self.get_cardinality(relation)
                    key_pair = (left_key, right_key)

                    self.total_result[key_pair].append(result)
                    self.cardinality_result[card][key_pair].append(result)
                    self.results[relation][key_pair].append(result)

    def single_comparison(self, features:  Dict[str, torch.Tensor], left_key: str, right_key: str,
                          relation: str, sub: str, obj: str):
        left_features: torch.Tensor = features[left_key]
        right_features: torch.Tensor = features[right_key]
        result = self.metric(left_features, right_features)

        if self.persist is not None:
            try:
                self.persist(left_key, right_key, relation, sub, obj, result)
                if self.is_symmetric:
                    self.persist(right_key, left_key, relation, sub, obj, result)
            except Exception as exception:
                print(exception)
        return result

    def get_key_pairs(self) -> List[Tuple[str, str]]:
        if self.is_symmetric:
            key_pairs: List[Tuple[str, str]] = []
            for left in self.keys:
                for right in self.keys:
                    if (right, left) not in key_pairs:
                        key_pairs.append((left, right))
            return key_pairs
        return [(left, right) for left in self.keys for right in self.keys]

    def get_features(self, relation: str, sub: str) -> Dict[str, torch.Tensor]:
        sentences: Dict[str, str] = self.templater(relation, sub, self.mask, self.keys)
        features: Dict[str, torch.Tensor] = {}
        for key in self.keys:
            sentence: str = sentences[key]
            single_feature: torch.Tensor = self.extract_mask_features(sentence)
            features[key] = single_feature
        return features


