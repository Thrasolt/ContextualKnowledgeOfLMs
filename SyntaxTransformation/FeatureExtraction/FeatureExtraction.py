from typing import Callable
import torch


class FeatureExtraction:

    def __init__(self, tokenizer: Callable, model: Callable, mask: str):
        self.tokenizer = tokenizer
        self.model = model
        self.mask = mask
        self.mask_id = tokenizer({self.mask})['input_ids'][1]

    def extract_mask_features(self, sentence: str):
        index = self.tokenizer(sentence)['input_ids'].index(self.mask_id)
        return torch.tensor(self.model(sentence)[0][index])

