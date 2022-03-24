from typing import Dict, Tuple, List

import torch
from torch import nn
from transformers import pipeline, Pipeline

from LamaPrompts import LamaPrompts
from LamaTRExData import RELATIONS
from Timer import Timer

BERT_VOCAB_SIZE = 30522
ZERO_TENSOR = torch.zeros(BERT_VOCAB_SIZE)


def prompts_to_scores(score_objs) -> torch.Tensor:
    scores = torch.clone(ZERO_TENSOR)
    for score_obj in score_objs:
        scores[score_obj["token"]] = score_obj["score"]
    return scores


def flatten(lst: List) -> List:
    return [item for sublist in lst for item in sublist]


class PromptModel(nn.Module):
    def __init__(self, language_model: Pipeline, category: str, data: LamaPrompts) -> None:
        super().__init__()
        self.language_model: Pipeline = language_model
        self.category: str = category
        self.prompts: LamaPrompts = data
        self.prompts.load()
        self.params = nn.ParameterDict(self.get_parameters())
        self.timer = Timer()

    def get_parameters(self) -> Dict[str, nn.Parameter]:
        params: Dict[str, nn.Parameter] = {}
        for relation in RELATIONS:
            param_size: int = self.prompts.relation_size[self.category][relation]
            params[relation] = nn.Parameter(torch.randn(param_size))
        return params

    def generate_prompts(self, subject: str, relation: str) -> List[str]:
        generated_prompts: List[Tuple[str, float]] = self.prompts.generate_for_rel(self.category, relation, subject)
        return [prompt for prompt, weight in generated_prompts]

    def forward(self, subjects: List[str], rels: List[str]) -> torch.tensor:
        self.timer.timeit("start")

        output: torch.tensor = torch.zeros(len(subjects), BERT_VOCAB_SIZE)
        all_prompts: List[str] = flatten([self.generate_prompts(sub, rel) for sub, rel in zip(subjects, rels)])
        all_rels: List[str] = flatten([[rel] * self.prompts.relation_size[self.category][rel] for rel in rels])
        self.timer.timeit("prompts")
        prompt_output = self.language_model(all_prompts)
        self.timer.timeit("pipline")

        current_relation = all_rels[0]
        current_index = 0
        rel_prompt_weight_index = 0
        current_agg_score = torch.zeros(BERT_VOCAB_SIZE)
        for line_index, score_object in enumerate(prompt_output):
            if all_rels[line_index] != current_relation or rel_prompt_weight_index >= self.prompts.relation_size[self.category][current_relation]:
                output[current_index] = current_agg_score
                current_agg_score = torch.zeros(BERT_VOCAB_SIZE)
                current_index += 1
                current_relation = all_rels[line_index]
                rel_prompt_weight_index = 0

            current_agg_score += prompts_to_scores(score_object) * self.params[current_relation][rel_prompt_weight_index]
            rel_prompt_weight_index += 1
        self.timer.timeit("preprocessing")

        """
        output: torch.tensor = torch.zeros(len(subject_list), BERT_VOCAB_SIZE)
        for index, (sub, rel) in enumerate(zip(subject_list, relation_list)):
            output[index] = self.forward_single(sub, rel)
        """
        return output

    @torch.no_grad()
    def forward_single(self, subject_label: str, relation: str) -> torch.tensor:
        generated_prompts: List[str] = self.generate_prompts(subject_label, relation)
        sum_of_scores = torch.zeros(BERT_VOCAB_SIZE).float()
        prompt_output = self.language_model(generated_prompts)

        for index in range(len(generated_prompts)):
            scores = prompts_to_scores(prompt_output[index])
            sum_of_scores += self.params[relation][index] * scores
        return sum_of_scores


