import configparser
import json
import os

from typing import List, Dict, Tuple

OBJ_LABEL = "obj_label"
SUB_LABEL = "sub_label"

config = configparser.ConfigParser()
config.read('configuration.ini')

RELATIONS = ["P1376", "P36", "P1001", "P103", "P131", "P140", "P159", "P19", "P20", "P276", "P30", "P364", "P449",
            "P495", "P740", "P101", "P106", "P108", "P127", "P1303", "P136", "P138", "P1412", "P17", "P176", "P178",
            "P190", "P264", "P27", "P279", "P31", "P361", "P37", "P39", "P407", "P413", "P463", "P47", "P527", "P530",
            "P413", "P937"]

relation_cardinality = {
    "1:1": ["P1376", "P36"],
    "n:1": ["P1001", "P103", "P131", "P140", "P159", "P19", "P20", "P276", "P30", "P364", "P449", "P495",
            "P740"],
    "n:m": ["P101", "P106", "P108", "P127", "P1303", "P136", "P138", "P1412", "P17", "P176", "P178",
            "P190", "P264", "P27", "P279", "P31", "P361", "P37", "P39", "P407", "P413", "P463",
            "P47", "P527", "P530", "P413", "P937"]
}


def remove_suffix(string: str, suffix: str) -> str:
    if suffix in string:
        return string[:-len(suffix)]
    return string


def load_triples_for_relation(file_path: str) -> List[Tuple[str, str]]:
    extracted_file_data: List[Tuple[str, str]] = []
    with open(file_path) as file:
        for line in file:
            extracted_file_data.append(extract_data_from_line(line))
    return extracted_file_data


def extract_data_from_line(line: str) -> Tuple[str, str]:
    line_content = json.loads(line)
    return line_content[SUB_LABEL], line_content[OBJ_LABEL]


class LamaTRExData:
    def __init__(self, train: bool = False, relations=None) -> None:
        self.relations = RELATIONS if relations is None else relations
        self.data_dir: str = config["locations"]["train_data_dir"] if train else config["locations"]["test_data_dir"]
        self.data: Dict = {rel: [] for rel in self.relations}
        self.data_set: List[Tuple[Tuple[str, str], str]] = []

    def load(self) -> None:
        for file_name in os.listdir(self.data_dir):
            relation = remove_suffix(file_name, ".jsonl")
            self.load_relation(file_name, relation)
            self.create_data_matrix()

    def load_relation(self, file_name, relation) -> None:
        if relation in self.relations:
            file_path: str = os.path.join(self.data_dir, file_name)
            self.data[relation] = load_triples_for_relation(file_path)

    def create_data_matrix(self) -> None:
        for relation, pair in self.data.items():
            for subj, obj in pair:
                self.data_set.append(((subj, relation), obj))


