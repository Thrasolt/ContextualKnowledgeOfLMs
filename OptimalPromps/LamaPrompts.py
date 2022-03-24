import configparser
import json
import os

from LamaTRExData import remove_suffix, RELATIONS
from typing import List, Dict, Tuple

config = configparser.ConfigParser()
config.read('configuration.ini')

MASK = "[MASK]"
CATEGORIES = ["mine", "paraphrase"] #manual_paraphrase


def parse_template(line: str) -> Tuple[str, float]:
    content = json.loads(line)
    return content["template"], content["weight"]


def load_template_for_prompt_category(file_path: str) -> List[Tuple[str, float]]:
    with open(file_path) as file:
        return list(map(parse_template ,file.readlines()))


class LamaPrompts:

    def __init__(self) -> None:
        self.prompt_dir: str = config["locations"]["prompt_dir"]
        self.sub_placeholder: str = config["prompts"]["subject_placeholder"]
        self.obj_placeholder: str = config["prompts"]["object_placeholder"]
        self.prompts: Dict = {category: {relation: [] for relation in RELATIONS} for category in CATEGORIES}
        self.relation_size: Dict = {category: {relation: 0 for relation in RELATIONS} for category in CATEGORIES}

    def load(self) -> None:
        for category in CATEGORIES:
            self.load_for_category(category)

    def load_for_category(self, category: str) -> None:
        category_path: str = os.path.join(self.prompt_dir, category)
        for file_name in os.listdir(category_path):
            relation_path: str = os.path.join(category, category_path, file_name)
            self.load_relation(category, relation_path, file_name)

    def load_relation(self, category, relation_path, file_name) -> None:
        relation = remove_suffix(file_name, ".jsonl")
        if relation in RELATIONS:
            self.prompts[category][relation] = load_template_for_prompt_category(relation_path)
            self.relation_size[category][relation] = len(self.prompts[category][relation])

    def generate_for_rel(self, category: str, relation: str, subject_label: str) -> List[Tuple[str, float]]:
        templates: List[Tuple[str, float]] = self.prompts[category][relation]
        prompts: List[Tuple[str, float]] = []
        for template, weight in templates:
            prompt = template.replace(self.sub_placeholder, subject_label).replace(self.obj_placeholder, MASK)
            prompts.append((prompt, weight))
        return prompts





