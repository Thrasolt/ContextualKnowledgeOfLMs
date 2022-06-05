from typing import List, Dict, Tuple, Callable

import numpy as np
import torch
import torch.nn as nn

cos: Callable[[torch.Tensor, torch.Tensor],  torch.Tensor] = nn.CosineSimilarity(dim=0, eps=1e-6)


@torch.no_grad()
def calculate_similarity_matrix(embeddings: List[torch.Tensor],
                                metric: Callable[[torch.Tensor, torch.Tensor],  torch.Tensor]) -> np.ndarray:

    similarity_matrix = np.zeros((4, 4))
    for row, right_embedding in enumerate(embeddings):
        for col, left_embedding in enumerate(embeddings):
            similarity_matrix[row, col] = metric(left_embedding, right_embedding).item()
    return similarity_matrix


class TypologyEmbeddingComparisonUnit:
    def __init__(self, sub_label: str, obj_label: str, embeddings: List[torch.Tensor],
                 metric: Callable[[torch.Tensor, torch.Tensor],  torch.Tensor]):
        self.sub_label: str = sub_label
        self.obj_label: str = obj_label
        self.similarity_matrix: np.ndarray = calculate_similarity_matrix(embeddings, metric)

    def get(self) -> Tuple[str, str, np.ndarray]:
        return self.sub_label, self.obj_label, self.similarity_matrix


class TypologyEmbeddingComparison:
    def __init__(self, relations: List[str], metric: Callable[[torch.Tensor, torch.Tensor],  torch.Tensor] = cos):
        self.results: Dict[str, List[TypologyEmbeddingComparisonUnit]] = {relation: [] for relation in relations}
        self.metric: Callable[[torch.Tensor, torch.Tensor],  torch.Tensor] = metric

    def process_embeddings(self, relation: str, sub_label: str, obj_label: str, embeddings: List[torch.Tensor]):
        comparison_unit = TypologyEmbeddingComparisonUnit(sub_label, obj_label, embeddings, self.metric)
        self.results[relation].append(comparison_unit)

    def show_similarity(self, relation: str, first_type: int, second_type: int):
        print(f"Similarities for {relation} type {first_type} vs type {second_type}:")
        for unit in self.results[relation]:
            sub_label, obj_label, similarity_matrix = unit.get()
            print(f"{sub_label}, {obj_label}: {similarity_matrix[first_type-1, second_type-1]} ")
