from typing import List, Dict, Union
import torch


def get_distribution_from_pipeline(model_output: List[Dict[str, Union[str, float]]]) -> torch.Tensor:
    distribution: List[float] = [output["score"] for output in model_output]
    return torch.tensor(distribution)


def get_probability_from_pipeline_for_token(model_output: List[Dict[str, Union[str, float]]], token: str) -> float:
    try:
        return list(filter(lambda token_result: token_result["token_str"] == token, model_output))[0]["score"]
    except IndexError as err:
        return 0.0

