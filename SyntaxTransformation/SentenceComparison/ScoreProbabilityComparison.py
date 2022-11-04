from typing import Callable, List, Dict, Tuple

import numpy as np
from matplotlib import pyplot as plt



from .constants import KEYS, CARDINALITIES
from .SentenceComparison import SentenceComparison, create_initial_results


def calculate_score_probability_function(score_data: List[float], number_of_bins: int) -> Callable[[float], float]:
    bins: Dict[int, List[float]] = {bin_number: [] for bin_number in range(number_of_bins)}

    for score in score_data:
        bin_number: int = place_score(number_of_bins, score)
        bins[bin_number].append(score)

    probability: Dict[int, float] = {bin_number: len(value)/len(score_data) if len(score_data) > 0 else 0
                                     for bin_number, value in bins.items()}
    return lambda token_score: probability[place_score(number_of_bins, token_score)]


def place_score(number_of_bins, score) -> int:
    for bin_number in range(number_of_bins):
        left_boundary: float = bin_number / number_of_bins
        right_boundary: float = (bin_number + 1) / number_of_bins
        if left_boundary <= score < right_boundary:
            return bin_number


def create_plot_data(x_values: List[float], y_values: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    data: List[Tuple[float, float]] = list(zip(x_values, y_values))
    data: List[Tuple[float, float]]  = sorted(data, key=lambda point: point[0])
    data: np.ndarray = np.array(data)
    return data[:, 0], data[:, 1]


class ScoreProbabilityComparison(SentenceComparison):

    def __init__(self,
                 relations: List[str],
                 templater: Callable[[str, str, str], Dict[str, str]],
                 score_metric: Callable,
                 mask: str,
                 get_relation_meta: Callable,
                 number_of_bins: int,
                 keys=None):
        if keys is None:
            keys = KEYS
        super().__init__(relations, templater, score_metric, mask, get_relation_meta, keys)
        self.number_of_bins: int = number_of_bins
        self.score_probability_functions: Dict[str, Callable[[float], float]] = {}
        self.total_score_probability: Dict[str, List[float]] = {}
        self.cardinality_score_probability: Dict[str, Dict[str, List[float]]] = create_initial_results(
            CARDINALITIES, self.keys)
        self.relation_score_probability: Dict[str, Dict[str, List[float]]] = create_initial_results(
            self.relations, self.keys)

    def calculate_probability_data(self, key: str):
        self.total_score_probability[key] = [
            self.score_probability_functions[key](score) for score in self.total_result[key]]

    def compare_for_card(self):
        for card in CARDINALITIES:
            for key in self.keys:
                prob_fun: Callable = calculate_score_probability_function(
                    self.cardinality_result[card][key], self.number_of_bins)
                self.cardinality_score_probability[card][key] = [
                    prob_fun(score) for score in self.cardinality_result[card][key]]

    def compare_for_relations(self):
        for rel in self.relations:
            for key in self.keys:
                prob_fun: Callable = calculate_score_probability_function(
                    self.results[rel][key], self.number_of_bins)
                self.relation_score_probability[rel][key] = [
                    prob_fun(score) for score in self.results[rel][key]]

    def compare(self, triples: Dict[str, List[Tuple[str, str]]]):
        super(ScoreProbabilityComparison, self).compare(triples)
        self.score_probability_functions = {key: calculate_score_probability_function(
            self.total_result[key], self.number_of_bins) for key in self.keys}
        for key in self.keys:
            self.calculate_probability_data(key)
        self.compare_for_card()
        self.compare_for_relations()

    def plot_global_comparison(self):
        fig, ax = plt.subplots()
        ax.set(xlabel='score', ylabel="score-probability")

        ax.set_title("Global score vs score probability")
        ax.set_ylim([0, 0.05])

        for key in self.keys:
            x_values, y_values = create_plot_data(self.total_result[key], self.total_score_probability[key])
            ax.plot(x_values, y_values, label=f"{key}")

        ax.legend(loc='upper center')
        plt.show()

    def plot_cardinality_comparison(self, y_limit=None):
        for card in CARDINALITIES:
            x_data: Dict[str, List[float]] = self.cardinality_result[card]
            y_data: Dict[str, List[float]] = self.cardinality_score_probability[card]
            self.plot_for_category(card, x_data, y_data, y_limit)

    def plot_relation_comparison(self, y_limit=None):
        for rel in self.relations:
            x_data: Dict[str, List[float]] = self.results[rel]
            y_data: Dict[str, List[float]] = self.relation_score_probability[rel]
            title_appendix: str = f"{self.get_relation_meta(rel)} - {len(list(x_data.values())[0])}"
            self.plot_for_category(rel, x_data, y_data, y_limit, title_appendix)

    def plot_for_category(self, category: str, x_data: Dict[str, List[float]],
                          y_data: Dict[str, List[float]], y_limit: Tuple[float, float] = None, title_appendix: "str" = ""):
        fig, ax = plt.subplots()
        if y_limit is not None:
            ax.set_ylim(y_limit)
        ax.set(xlabel='score', ylabel="score-probability")
        ax.set_title(f"Score vs score probability for {category} {title_appendix}")

        for key in self.keys:
            x_values, y_values = create_plot_data(x_data[key], y_data[key])
            ax.plot(x_values, y_values, label=f"{key}")
        ax.legend(loc='upper center')
        plt.show()







