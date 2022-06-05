# P101
# field of work
from typing import List, Callable


def template_level_1(sub_label: str, object_label: str) -> str:
    #return f"{sub_label}'s field of work was {object_label}."
    return f"{sub_label} works in the domain of {object_label}"


def template_level_2(sub_label: str, object_label: str) -> str:
    return f"{sub_label} was known in his field of work and his particular field was {object_label}"


def template_level_3(sub_label: str, object_label: str) -> str:
    return f"People in his time knew {object_label}'s field of work, which was {sub_label}"


def template_level_4(sub_label: str, object_label: str) -> str:
    return f"{sub_label} was known in his discipline for the work he had done in his field and the subject of his work was {object_label}"


templates: List[Callable[[str, str], str]] = [template_level_1, template_level_2, template_level_3, template_level_4]


def retrieve_all_prompts(sub_label: str, object_label: str) -> List[str]:
    return [template_function(sub_label, object_label) for template_function in templates]