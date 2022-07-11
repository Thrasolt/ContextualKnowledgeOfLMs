import json
from os.path import isfile, join
from typing import Dict, List
from os import listdir

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"

SUBJ_LABEL = "[SUBJ_LABEL]"
OBJ_LABEL = "[OBJ_LABEL]"

KEYS = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

PROJECT_PATH = "/Users/tim/projects/ContextualKnowledgeOfLMs/SyntaxTransformation"
RELATIONS_PATH = f"{PROJECT_PATH}/relation_templates/relations"

relations = [file_name.split(".json")[0] for file_name in
             [file_name for file_name in listdir(RELATIONS_PATH) if isfile(join(RELATIONS_PATH, file_name))]]

nominalized_relations = ["P127", "P136", "P176", "P178", "P413", "P1303"]

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
