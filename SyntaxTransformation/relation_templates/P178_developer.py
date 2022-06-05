# P178
# developer
from typing import List, Callable


def template_level_1(sub_label: str, object_label: str) -> str:
    return f"{sub_label} was created by {object_label}."


def template_level_2(sub_label: str, object_label: str) -> str:
    return f"{object_label} is developing something and an example of such a development is {sub_label}"


def template_level_3(sub_label: str, object_label: str) -> str:
    return f"As a developer {object_label} has developed {sub_label}"


def template_level_4(sub_label: str, object_label: str) -> str:
    return f"{object_label} is known for the things it develops and it has developed something, that is called {sub_label}"


templates: List[Callable[[str, str], str]] = [template_level_1, template_level_2, template_level_3, template_level_4]


def retrieve_all_prompts(sub_label: str, object_label: str) -> List[str]:
    return [template_function(sub_label, object_label) for template_function in templates]