# P103
# native language
from typing import List, Callable


def template_level_1(sub_label: str, object_label: str) -> str:
    return f"The native language of {sub_label} is {object_label}"


def template_level_2(sub_label: str, object_label: str) -> str:
    return f"{sub_label} speaks {object_label} and it is also his native language"


def template_level_3(sub_label: str, object_label: str) -> str:
    return f"{sub_label} has a native language, which is {object_label}"


def template_level_4(sub_label: str, object_label: str) -> str:
    return f"{sub_label} speaks {object_label} and he speaks it well because it is his native language"


templates: List[Callable[[str, str], str]] = [template_level_1, template_level_2, template_level_3, template_level_4]


def retrieve_all_prompts(sub_label: str, object_label: str) -> List[str]:
    return [template_function(sub_label, object_label) for template_function in templates]