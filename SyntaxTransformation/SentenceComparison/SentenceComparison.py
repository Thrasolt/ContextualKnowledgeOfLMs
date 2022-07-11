from typing import Dict, List, Tuple, Callable
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"
KEYS: List[str] = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

ONE_TO_ONE = "1:1"
N_TO_ONE = "N:1"
N_TO_M = "N:M"
CARDINALITIES = [ONE_TO_ONE, N_TO_ONE, N_TO_M]


def create_initial_results(keys: List[str]) -> Dict[str, Dict[str, List[float]]]:
    results = {}
    for relation in keys:
        results[relation] = {}
        for key in KEYS:
            results[relation][key] = []
    return results


class SentenceComparison:
    def __init__(self,
                 relations: List[str],
                 templater: Callable[[str, str, str], Dict[str, str]],
                 metric: Callable,
                 mask: str,
                 get_relation_meta: Callable):
        self.relations: List[str] = relations
        self.templater: Callable[[str, str, str], Dict[str, str]] = templater
        self.metric: Callable = metric
        self.mask: str = mask
        self.results: Dict = create_initial_results(self.relations)
        self.total_result: Dict[str, List[float]] = {key: [] for key in KEYS}
        self.cardinality_result: Dict = create_initial_results(CARDINALITIES)
        self.get_relation_meta = get_relation_meta

    def compare(self, triples: Dict[str, List[Tuple[str, str]]]):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation]):
                sentences: Dict[str, str] = self.templater(relation, sub, self.mask)
                for key in KEYS:
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
            means: List[float] = [np.mean(self.results[relation][key]).item() for key in KEYS]
            row: List[str] = [relation] + ["{:.3f}".format(mean) for mean in means]
            rows.append(row)
        return rows

    def print_global_for_latex(self):
        rows: List[List[str]] = self.make_global_comparison()
        rows = sorted(rows, key=lambda lst: int(lst[0][1:]))
        for row in rows:
            print(" & ".join(row) + "\\\\")