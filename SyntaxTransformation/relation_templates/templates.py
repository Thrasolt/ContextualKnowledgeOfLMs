import json
import math
from os.path import isfile, join
from typing import Dict, List, Union, Callable
from os import listdir
import re

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"

SUBJ_LABEL = "[SUBJ_LABEL]"
OBJ_LABEL = "[OBJ_LABEL]"

SUB_TOKEN = 2548
OBJ_TOKEN = 4231

KEYS = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

CARDINALITIES = ["1:1", "N:1", "N:M"]

PROJECT_PATH = "/Users/tim/projects/ContextualKnowledgeOfLMs/SyntaxTransformation"
RELATIONS_PATH = f"{PROJECT_PATH}/relation_templates/relations"

relations = [file_name.split(".json")[0] for file_name in
             [file_name for file_name in listdir(RELATIONS_PATH) if isfile(join(RELATIONS_PATH, file_name))]]

nominalized_relations = ["P127", "P136", "P176", "P178", "P413", "P1303"]

abstract_relations = ['P138', 'P276', 'P31', 'P937', 'P279', 'P527', 'P101', 'P361']

relation_names: Dict[str, str] = {}
relation_cardinality: Dict[str, str] = {}


def update_relation_meta_info(relation: str, name: str, cardinality: str):
    relation_names[relation] = name
    relation_cardinality[relation] = cardinality


def get_relation_name(relation: str) -> str:
    assert relation in relation_names, "relation not available"
    return relation_names[relation]


def get_relation_cardinality(relation: str) -> str:
    if relation == "total":
        return ""
    assert relation in relation_names, "relation not available"
    return relation_cardinality[relation]


def get_relation_meta(relation: str) -> str:
    assert relation in relation_names, "relation not available"
    return f"{relation_names[relation]} {relation_cardinality[relation]}"


def insert_into_template(template: str, sub: str, obj: str) -> str:
    return template.replace(SUBJ_LABEL, sub).replace(OBJ_LABEL, obj)


def get_templates(relation: str, sub: str, obj: str, keys=None) -> Dict[str, str]:
    if keys is None:
        keys = KEYS
    with open(f"{PROJECT_PATH}/relation_templates/relations/{relation}.json") as file:
        raw_templates: Dict[str, str] = json.load(file)

        update_relation_meta_info(relation, raw_templates["name"], raw_templates["cardinality"])

        templates: Dict[str, str] = {}
        for key in keys:
            templates[key] = insert_into_template(raw_templates[key], sub, obj)

        return templates


def get_template_list(relation: str, sub: str, obj: str) -> List[str]:
    return list(get_templates(relation, sub, obj).values())


def get_all_templates() -> List[str]:
    templates: List[str] = []
    for relation in relations:
        current_templates: List[str] = list(get_templates(relation, SUBJ_LABEL, OBJ_LABEL).values())
        templates.append(f"{relation}: {get_relation_name(relation)}")
        for template in current_templates:
            templates.append(template)
    return templates


def get_length_for_relation(tokenizer: Callable, keys: List[str] = None) -> List[List[Union[str, int]]]:
    if keys is None:
        keys = KEYS
    rows: List[List[Union[str, int]]] = []
    for relation in relations:
        row: List[Union[str, int]] = [relation]
        templates: Dict = get_templates(relation, "foo", "bar", keys)
        for key in keys:
            row.append(len(tokenizer(templates[key])))
        rows.append(row)
    rows = sorted(rows, key=lambda row: row[0])
    return [["relations"] + keys] + rows


def get_order_for_relation(tokenizer: Callable, keys: List[str] = None):
    if keys is None:
        keys = KEYS
    metric: Callable = lambda sentence: int(sentence.find("subject") < sentence.find("object"))
    return metric_for_relation(keys, metric)


def get_distance_for_relation(tokenizer: Callable, keys: List[str] = None) -> List[List[Union[str, int]]]:
    if keys is None:
        keys = KEYS
    metric: Callable = lambda sentence: abs(tokenizer(sentence).index(SUB_TOKEN) - tokenizer(sentence).index(OBJ_TOKEN))
    return metric_for_relation(keys, metric)


def starts_with_mask(keys: List[str] = None):
    if keys is None:
        keys = KEYS
    metric: Callable = lambda sentence: 0 if sentence.find("object") == 0 else 1
    return metric_for_relation(keys, metric)


def starts_with_sub(keys: List[str] = None):
    if keys is None:
        keys = KEYS
    metric: Callable = lambda sentence: 1 if sentence.find("subject") == 0 else 0
    return metric_for_relation(keys, metric)


def metric_for_relation(keys: List[str], metric: Callable[[str], int]) -> List[List[Union[str, int]]]:
    rows: List[List[Union[str, int]]] = []
    for relation in relations:
        row: List[Union[str, int]] = [relation]
        templates: Dict = get_templates(relation, "subject", "object", keys)
        for key in keys:
            row.append(metric(templates[key]))
        rows.append(row)
    return [["relations"] + keys] + rows


def get_relations_with_last_digit(digit: int):
    assert 0 <= digit <= 9, "digit must be a single digit"
    return list(filter(lambda rel: rel[-1] == str(digit), relations))


def get_relations_for_cardinalities(relationList: List[str]) -> Dict[str, List[str]]:
    res: Dict[str, List[str]] = {card: [] for card in CARDINALITIES}

    for relation in relationList:
        res[get_relation_cardinality(relation)].append(relation)

    return res


