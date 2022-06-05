# P36
# place of birth
from typing import List, Callable


def template_level_1(sub_label: str, object_label: str) -> str:
    return f"{object_label} is the capital of {sub_label}."


def template_level_2(sub_label: str, object_label: str) -> str:
    return f"{sub_label} has a capital and the capital is {object_label}."


def template_level_3(sub_label: str, object_label: str) -> str:
    return f"It was happening in {object_label} which is it's capital {sub_label} "


def template_level_4(sub_label: str, object_label: str) -> str:
    return f"It was called {object_label} and she was there because it is the capital of {sub_label}."


templates: List[Callable[[str, str], str]] = [template_level_1, template_level_2, template_level_3, template_level_4]


def retrieve_all_prompts(sub_label: str, object_label: str) -> List[str]:
    return [template_function(sub_label, object_label) for template_function in templates]
