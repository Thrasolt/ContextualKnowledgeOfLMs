from inspect import signature, Signature
from typing import List, Callable, Dict, Tuple

from tqdm import tqdm

from .DistributionComparisonResult import DistributionComparisonResult
from .Constants import KEYS, SUBJ_LABEL


class SentenceTypologyEmbeddingDistributionComparison:
    def __init__(self,
                 relations: List[str],
                 templater: Callable[[str, str, str], Dict[str, str]],
                 words: List[str],
                 metric: Callable,
                 mask: str,
                 get_relation_meta: Callable,
                 title_name: str = "KL-divergence"):
        self.relations: List[str] = relations
        self.templater: Callable[[str, str, str], Dict[str, str]] = templater
        self.words: List[str] = words
        self.metric: Callable = metric
        self.mask: str = mask
        self.results: DistributionComparisonResult = DistributionComparisonResult(
            self.relations, self.words, title_name, get_relation_meta)

    def compare(self, triples: Dict[str, List[Tuple[str, str]]], max_triplets: int):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation][:max_triplets]):
                for word in self.words + [sub]:
                    left_sentences: Dict[str, str] = self.templater(relation, sub, self.mask)
                    right_sentences: Dict[str, str] = left_sentences
                    if sub != word:
                        right_sentences: Dict[str, str] = self.templater(relation, word, self.mask)
                    for left_key in KEYS:
                        for right_key in KEYS:
                            comparison: float = self.calculate_metric(
                                left_sentences[left_key], right_sentences[right_key], obj)

                            word_label = word if word != sub else SUBJ_LABEL
                            self.results.process_comparison(
                                relation, left_key, word_label, right_key, comparison)

    def calculate_metric(self, left_sentence: str, right_sentence: str, label: str) -> float:
        if self.is_label_required():
            comparison: float = self.metric(left_sentence, right_sentence, label)
        else:
            comparison = self.metric(left_sentence, right_sentence)
        return comparison

    def print_comparison(self, relation: str, sub_word: str, key_pairs: List[Tuple[str, str]]):
        self.results.print_single_comparison(relation, sub_word, key_pairs)

    def print_global_comparison(self):
        self.results.print_global_comparison()

    def print_global_for_latex(self):
        self.results.print_global_for_latex()

    def is_label_required(self) -> bool:
        sig: Signature = signature(self.metric)
        num_of_params: int = len(sig.parameters)
        return num_of_params == 3
