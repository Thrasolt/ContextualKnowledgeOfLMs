from typing import List, Dict, Tuple

import numpy as np

from .Constants import KEYS, SUBJ_LABEL
import matplotlib.pyplot as plt


class DistributionComparisonObject:
    def __init__(self, relation: str, left_key: str, sub_word: str, right_key: str):
        self.relation: str = relation
        self.left_key: str = left_key
        self.sub_word: str = sub_word
        self.right_key: str = right_key
        self.comparisons: List[float] = []

    def add(self, comparison_value: float):
        self.comparisons.append(comparison_value)

    def __hash__(self) -> int:
        return hash((self.relation, self.left_key, self.sub_word, self.right_key))


def create_result_dict(relations: List[str], words: List[str]) -> Dict[int, DistributionComparisonObject]:
    result: Dict[int, DistributionComparisonObject] = {}
    for relation in relations:
        for left_key in KEYS:
            for left_word in words + [SUBJ_LABEL]:
                for right_key in KEYS:
                    comparison_obj: DistributionComparisonObject = DistributionComparisonObject(
                        relation, left_key, left_word, right_key)
                    result[hash(comparison_obj)] = comparison_obj

    return result


def create_plot(title: str, data_sets: List[Tuple[np.ndarray, np.ndarray, str]]):
    fig, ax = plt.subplots()
    ax.set(xlabel='triplet nr.', ylabel='KL divergence', title=title)
    for x_data, y_data, label in data_sets:
        ax.plot(x_data, y_data, label=label)
    ax.legend()
    plt.show()


class DistributionComparisonResult:
    def __init__(self, relations: List[str], words: List[str]):
        self.relations: List[str] = relations
        self.words: List[str] = words
        self.results: Dict[int, DistributionComparisonObject] = create_result_dict(self.relations, self.words)

    def process_comparison(self, relation: str,
                           left_key: str, sub_word: str,
                           right_key: str, comparison: float):
        hash_key: int = hash((relation, left_key, sub_word, right_key))
        self.results[hash_key].add(comparison)

    def get_comparison(self, relation: str, left_key: str, left_word: str, right_key: str
                       ) -> DistributionComparisonObject:
        hash_key: int = hash((relation, left_key, left_word, right_key))
        return self.results[hash_key]

    def create_datasets(self, left_key: str, sub_word: str, right_word: str
                        ) -> List[Tuple[np.ndarray, np.ndarray, str]]:
        data_sets: List[Tuple[np.ndarray, np.ndarray, str]] = []
        for relation in self.relations:
            comparisons: List[float] = self.get_comparison(relation, left_key, sub_word, right_word).comparisons
            x_data: np.ndarray = np.arange(len(comparisons))
            y_data: np.ndarray = np.array(comparisons)
            data_sets.append((x_data, y_data, relation))
        return data_sets

    def print_comparison(self, left_key: str, sub_word: str, right_key: str):
        title: str = f"KL-divergence for {sub_word} {left_key} vs. {right_key}"
        data_sets: List[Tuple[np.ndarray, np.ndarray, str]] = self.create_datasets(
            left_key, sub_word, right_key)
        create_plot(title, data_sets)


