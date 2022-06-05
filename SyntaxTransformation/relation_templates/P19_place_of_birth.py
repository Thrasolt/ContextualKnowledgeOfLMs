# P19
# place of birth
from typing import List, Callable


def template_level_1(sub_label: str, object_label: str) -> str:
    return f"{sub_label} was born in {object_label}."


def template_level_2(sub_label: str, object_label: str) -> str:
    return f"{object_label} is the name of a place, {sub_label} was born there."


def template_level_3(sub_label: str, object_label: str) -> str:
    return f"{object_label} is the name of the place, where {sub_label} was born."


def template_level_4(sub_label: str, object_label: str) -> str:
    return f"{object_label} is the name of the place, where some people were born, for example {sub_label}."


templates: List[Callable[[str, str], str]] = [template_level_1, template_level_2, template_level_3, template_level_4]


def retrieve_all_prompts(sub_label: str, object_label: str) -> List[str]:
    return [template_function(sub_label, object_label) for template_function in templates]
