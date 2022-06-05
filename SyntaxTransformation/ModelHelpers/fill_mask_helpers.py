from typing import List, Dict, Union
import torch


def get_distribution_from_pipeline(model_output: List[Dict[str, Union[str, float]]]) -> torch.Tensor:
    distribution: List[float] = [output["score"] for output in model_output]
    return torch.tensor(distribution)
