from typing import Dict, Callable, List

from .P19_place_of_birth import retrieve_all_prompts as p19
from .P36_capital import retrieve_all_prompts as p36
from .P101_field_of_work import retrieve_all_prompts as p101
from .P178_developer import retrieve_all_prompts as p178
from .P103_native_language import retrieve_all_prompts as p103

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"

KEYS = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

functions_for_relations: Dict[str, Callable[[str, str], List[str]]] = {
    "P19": p19,
    "P36": p36,
    "P101": p101,
    "P103": p103,
    "P178": p178,
}

def templater(relation: str, sub: str, obj: str) -> List[str]:
    return functions_for_relations[relation](sub, obj)


def dict_templater(relation: str, sub: str, obj: str) -> Dict[str, str]:
    sentences: List[str] = templater(relation, sub, obj)
    return {key: template for (key, template) in zip(KEYS, sentences)}
