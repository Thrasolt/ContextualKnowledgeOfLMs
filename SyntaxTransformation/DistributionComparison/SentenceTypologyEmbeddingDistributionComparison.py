from typing import List, Callable, Dict, Tuple

import torch.nn as nn
from tqdm import tqdm

from .DistributionComparisonResult import DistributionComparisonResult
from .Constants import KEYS, SUBJ_LABEL


class SentenceTypologyEmbeddingDistributionComparison:
    def __init__(self,
                 relations: List[str],
                 templater: Callable[[str, str, str], Dict[str, str]],
                 words: List[str],
                 metric: Callable,
                 mask: str):
        self.relations: List[str] = relations
        self.templater: Callable[[str, str, str], Dict[str, str]] = templater
        self.words: List[str] = words
        self.metric: Callable = metric
        self.mask: str = mask
        self.results: DistributionComparisonResult = DistributionComparisonResult(self.relations, self.words)

    def compare(self, triples: Dict[str, List[Tuple[str, str]]], max_triplets: int):
        for relation in self.relations:
            for sub, obj in tqdm(triples[relation][:max_triplets]):
                for word in self.words + [sub]:
                    left_sentences: Dict[str, str] = self.templater(relation, sub, self.mask)
                    right_sentences: Dict[str, str] = self.templater(relation, word, self.mask)
                    for left_key in KEYS:
                        for right_key in KEYS:
                            comparison: float = self.metric(left_sentences[left_key], right_sentences[right_key])
                            word_label = word if word != sub else SUBJ_LABEL
                            self.results.process_comparison(
                                relation, left_key, word_label, right_key, comparison)

    def print_comparison(self, left_key: str, right_word: str, sub_word: str):
        self.results.print_comparison(left_key, sub_word, right_word)

