from typing import List, Dict, Tuple, Callable, Union

import numpy as np

from .Constants import KEYS, SUBJ_LABEL, VALID_KEY_COMBS
import matplotlib.pyplot as plt


MARKERS = [".", "x", ""]

class DistributionComparisonObject:
    def __init__(self, left_key: str, right_key: str):
        self.left_key: str = left_key
        self.right_key: str = right_key
        self.comparisons: List[float] = []

    def add(self, comparison_value: float):
        self.comparisons.append(comparison_value)

    def __hash__(self) -> int:
        return hash((self.left_key, self.right_key))


def create_result_dict(relations: List[str], words: List[str]) -> Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]]:
    result: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]] = {}
    for relation in relations:
        result[relation] = {}
        for word in words + [SUBJ_LABEL]:
            result[relation][word] = {}
            for left_key in KEYS:
                result[relation][word][left_key] = {}
                for right_key in KEYS:
                    result[relation][word][left_key][right_key] = []

    return result


def create_plot(title: str, data_sets: List[Tuple[np.ndarray, np.ndarray, str]], title_name: str,
                get_relation_meta: Callable):
    fig, ax = plt.subplots()
    ax.set(xlabel='triplet nr.', ylabel=title_name, title=title)
    for x_data, y_data, label in data_sets:
        ax.plot(x_data, y_data, label=f"{label}: {get_relation_meta(label)}")
    ax.legend(loc='upper right') #, bbox_to_anchor=(1, 0.5))
    plt.show()


class DistributionComparisonResult:
    def __init__(self, relations: List[str], words: List[str], title_name: str, get_relation_meta: Callable):
        self.relations: List[str] = relations
        self.words: List[str] = words
        self.results: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]] = create_result_dict(self.relations, self.words)
        self.title_name: str = title_name
        self.get_relation_meta = get_relation_meta

    def process_comparison(self, relation: str,
                           left_key: str, sub_word: str,
                           right_key: str, comparison: float):
        self.results[relation][sub_word][left_key][right_key].append(comparison)

    def get_comparison(self, relation: str, left_key: str, sub_word: str, right_key: str
                       ) -> List[float]:
        return self.results[relation][sub_word][left_key][right_key]

    def create_datasets(self,
                        relation: str, word: str,
                        key_pairs: List[Tuple[str, str]]) -> List[Tuple[str, str, List[float]]]:
        relation_word_result: Dict[str, Dict[str, List[float]]] = self.results[relation][word]
        return [(right_key, left_key, relation_word_result[right_key][left_key]) for right_key, left_key in key_pairs]

    def print_single_comparison(self, relation: str, word: str, key_pairs: List[Tuple[str, str]]):
        fig, ax = plt.subplots()
        ax.set(xlabel='triplet nr.', ylabel=self.title_name, title=self.title_name)

        datasets: List[Tuple[str, str, List[float]]] = self.create_datasets(relation, word, key_pairs)

        ax.set_title(f"{relation}:{self.get_relation_meta(relation)}")

        for index, (left_key, right_key, dataset) in enumerate(datasets):
            x_data: List[int] = list(range(len(dataset)))
            ax.scatter(x_data, dataset, marker=str((index % 4) + 1), label=f"{left_key} vs. {right_key}")

        ax.legend(loc='upper right') #, bbox_to_anchor=(1, 0.5))
        plt.show()

    def make_global_comparison(self, word: str) -> List[List[str]]:
        rows: List[List[str]] = []
        for relation in self.relations:
            datasets: List[Tuple[str, str, List[float]]] = self.create_datasets(relation, word, VALID_KEY_COMBS)
            data_means: List[Tuple[str, str, str]] = list(
                map(lambda triple: (triple[0], triple[1], "{:.3f}".format(np.mean(triple[2]).item())), datasets))
            row: List[str] = [relation] + [mean_diff for (_, _, mean_diff) in data_means]
            rows.append(row)
        return rows

    def print_global_comparison(self, word: str = SUBJ_LABEL):
        valid_combs_as_str: List[str] = [f"{left_key} vs. {right_key}" for left_key, right_key in VALID_KEY_COMBS]
        print("Relations " + " ".join(valid_combs_as_str))
        for row in self.make_global_comparison(word):
            print(" ".join(row))

    def print_global_for_latex(self, word: str = SUBJ_LABEL):
        rows: List[List[str]] = self.make_global_comparison(word)
        rows = sorted(rows, key=lambda lst: int(lst[0][1:]))
        for row in rows:
            print(" & ".join(row) + "\\\\")




