import torch


def kl_divergence(p_distribution: torch.Tensor, q_distribution: torch.Tensor) -> torch.Tensor:
    return (torch.log(p_distribution / q_distribution) * p_distribution).sum().item()


def jensen_shannon_divergence(p_distribution, q_distribution):
    mean_distribution: torch.Tensor = 0.5*p_distribution+0.5*q_distribution
    return 0.5*kl_divergence(p_distribution, mean_distribution) + 0.5*kl_divergence(q_distribution, mean_distribution)
