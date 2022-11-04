from __future__ import annotations

from typing import Dict, List, Tuple, Callable
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

from .constants import KEYS, CARDINALITIES


def create_initial_results(categories: List[str], keys: List[str]) -> Dict[str, Dict[str, List[float]]]:
    results = {}
    for cat in categories:
        results[cat] = {}
        for key in keys:
            results[cat][key] = []
    return results


class SentenceComparison:
    def __init__(self,
                 relations: List[str],
                 templater: Callable[[str, str, str], Dict[str, str]],
                 metric: Callable,
                 mask: str,
                 get_relation_meta: Callable,
                 keys=None):
        if keys is None:
            keys = KEYS
        self.relations: List[str] = relations
        self.templater: Callable[[str, str, str], Dict[str, str]] = templater
        self.metric: Callable = metric
        self.mask: str = mask
        self.keys: List[str] = keys
        self.results: Dict = create_initial_results(self.relations, self.keys)
        self.total_result: Dict[str, List[float]] = {key: [] for key in self.keys}
        self.cardinality_result: Dict = create_initial_results(CARDINALITIES, self.keys)
        self.get_relation_meta: Callable[[str], str] = get_relation_meta


    def compare(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation]):
                sentences: Dict[str, str] = self.templater(relation, sub, self.mask)
                for key in self.keys:
                    res: float = self.metric(sentences[key], obj)
                    card: str = self.get_relation_meta(relation).split(" ")[-1]
                    self.results[relation][key].append(res)
                    self.cardinality_result[card][key].append(res)
                    self.total_result[key].append(res)

    def plot_comparison_for_relation(self, relation: str, title: str):
        fig, ax = plt.subplots()
        ax.set(xlabel='triplet nr.', ylabel=title, title=title)

        ax.set_title(f"{relation}:{self.get_relation_meta(relation)}")

        for index, (key, dataset) in enumerate(self.results[relation].items()):
            x_data: List[int] = list(range(len(dataset)))
            ax.scatter(x_data, dataset, marker=str((index % 4) + 1), label=f"{key}")

        ax.legend(loc='upper right')
        plt.show()

    def make_global_comparison(self) -> List[List[str]]:
        rows: List[List[str]] = []
        for relation in self.relations:
            means: List[float] = [np.mean(self.results[relation][key]).item() for key in self.keys]
            row: List[str] = [relation] + ["{:.3f}".format(mean) for mean in means]
            rows.append(row)
        return rows

    def print_global_for_latex(self):
        rows: List[List[str]] = self.make_global_comparison()
        rows = sorted(rows, key=lambda lst: int(lst[0][1:]))
        for row in rows:
            print(" & ".join(row) + "\\\\")

    def plot_heat_map(self, metric: Callable, title: str):

        heat_values: np.ndarray = np.array(
            [[metric(self.total_result[left_key], self.total_result[right_key])
              for left_key in self.keys] for right_key in self.keys])

        fig, ax = plt.subplots()
        ax.imshow(heat_values)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        ax.set_xticks(np.arange(len(self.keys)), labels=self.keys)
        ax.set_yticks(np.arange(len(self.keys)), labels=self.keys)

        for row in range(len(self.keys)):
            for col in range(len(self.keys)):
                ax.text(col, row, heat_values[row, col], ha="center", va="center", color="w")

        ax.set_title(title)
        plt.show()

    def results_for_persistence(self) -> List[Tuple[str, None | str, float]]:
        rows: List[Tuple[str, None | str, float]] = []

        for key in self.keys:
            key_mean: float = np.mean(self.total_result[key]).item()
            if not np.isnan(key_mean):
                rows.append((key, None, key_mean))

            for card in CARDINALITIES:
                card_mean: float = np.mean(self.cardinality_result[card][key]).item()
                if not np.isnan(card_mean):
                    rows.append((key, card, card_mean))

            for rel in self.relations:
                rel_mean: float = np.mean(self.results[rel][key]).item()
                if not np.isnan(rel_mean):
                    rows.append((key, rel, rel_mean))

        return rows
