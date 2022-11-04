from __future__ import annotations

from typing import List, Dict, Tuple, Union
from tabulate import tabulate

import relation_templates.templates as templates


SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"
KEYS = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

ONE_TO_ONE = "1:1"
N_TO_ONE = "N:1"
N_TO_M = "N:M"
CARDINALITIES = [ONE_TO_ONE, N_TO_ONE, N_TO_M]

CORRECT = "correct"
TOTAL = "total"
ACCURACY = "accuracy"

HEADER_KEYS = [CORRECT, TOTAL, ACCURACY]

HEADERS = ['type', 'correct', 'total', "accuracy"]


def get_rel_card_from_str_row(row: str) -> str:
    cols: List[str] = row.split("&")
    return cols[2].strip() + cols[0].strip()


class RelationResult:
    def __init__(self, relation: str, top_k: int):
        self.relation: str = relation
        self.top_k: int = top_k
        self.correct_answers: int = 0
        self.total_answers: int = 0

    def process_answer(self, label: str, answers: List):
        for answer in answers[0:self.top_k]:
            if answer["token_str"] == label:
                self.correct_answers += 1
        self.total_answers += 1

    def print_result(self):
        print(f"total answers: {self.total_answers}")
        print(f"correct answers: {self.correct_answers}")
        print(f"accuracy: {self.correct_answers/self.total_answers * 100}%")

    def accuracy(self) -> float:
        try:
            return self.correct_answers/self.total_answers * 100
        except ZeroDivisionError as error:
            return 0.0

    def get(self) -> Dict[str, Union[int, float]]:
        return {CORRECT: self.correct_answers,
                TOTAL: self.total_answers,
                ACCURACY: self.accuracy()}

    def set_top_k(self, top_k: int):
        self.top_k = top_k


class TypologyResults:
    def __init__(self, relation: str, top_k: int, keys: List[str]):
        self.relation: str = relation
        self.top_k: int = top_k
        self.keys: List[str] = keys
        self.types: Dict[str, RelationResult] = {key: RelationResult(relation, top_k) for key in self.keys}

    def process_answers(self, label: str, answers: Dict[str, List]):
        for key, answer in answers.items():
            self.types[key].process_answer(label, answer)

    def print_result(self):
        for key in self.keys:
            self.types[key].print_result()

    def get(self) -> Dict[str, Dict[str, Union[int, float]]]:
        return {key: self.types[key].get() for key in self.keys}

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        for key in self.keys:
            self.types[key].set_top_k(top_k)


class SentenceTypologyQueryResults:
    def __init__(self, relations: List[str], top_k: int, keys: List[str]):
        self.top_k = top_k
        self.relations: List[str] = relations
        self.keys: List[str] = keys
        self.total_results: TypologyResults = TypologyResults("Total", self.top_k, self.keys)
        self.cardinality_results: Dict[str, TypologyResults] = self.init_cardinality_results()
        self.relation_results: Dict[str, TypologyResults] = self.init_relation_results()

    def init_cardinality_results(self):
        return {card: TypologyResults("Total", self.top_k, self.keys) for card in CARDINALITIES}

    def init_relation_results(self):
        relation_results: Dict[str, TypologyResults] = {}
        for relation in self.relations:
            relation_results[relation] = TypologyResults(relation, self.top_k, self.keys)
        return relation_results

    def process_answers(self, label: str, relation: str, answers: Dict[str, List]):
        if relation in self.relation_results.keys():
            self.relation_results[relation].process_answers(label, answers)
            card: str = templates.get_relation_cardinality(relation)
            self.cardinality_results[card].process_answers(label, answers)
        self.total_results.process_answers(label, answers)

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        self.total_results.set_top_k(top_k)
        for card in self.cardinality_results.values():
            card.set_top_k(top_k)
        for res in self.relation_results.values():
            res.set_top_k(top_k)

    def print_global_result(self):
        self.print_total()
        self.print_cardinalities()

    def print_result(self):
        for relation, result in self.relation_results.items():
            print(f"{relation}: {templates.get_relation_name(relation)} {templates.get_relation_cardinality(relation)}")

            rows: List[List[Union[str, int, float]]] = self.build_table_rows(relation)

            table = tabulate(rows, HEADERS, tablefmt='orgtbl')
            print(table)

    def print_total(self):
        rows: List[List[Union[str, int, float]]] = []
        for key, res in self.total_results.get().items():
            rows.append([key, *res.values()])
        table = tabulate(rows, HEADERS, tablefmt='orgtbl')
        print(f"total Result")
        print(table)

    def print_cardinalities(self):
        for card in self.cardinality_results.keys():
            rows: List[List[Union[str, int, float]]] = []
            for key, res in self.cardinality_results[card].get().items():
                rows.append([key, *res.values()])
            table = tabulate(rows, HEADERS, tablefmt='orgtbl')
            print(f"Total Result for {card}")
            print(table)

    def build_table_rows(self, relation) -> List[List[Union[str, int, float]]]:
        rows: List[List[Union[str, int, float]]] = []
        for key, res in self.relation_results[relation].get().items():
            rows.append([key, *res.values()])
        return rows

    def print_for_latex(self, header_key: str) -> List[str]:
        rows: List[str] = []
        for relation, result in self.relation_results.items():
            row: str = f"{relation} & {templates.get_relation_name(relation)} & {templates.get_relation_cardinality(relation)}"
            for key in self.keys:
                row = f"{row} & {result.get()[key][header_key]:.2f}"
            rows.append(f"{row} \\\\")

        return sorted(rows, key=get_rel_card_from_str_row)

    def print_global_latex(self, header_key: str) -> List[str]:
        rows: List[str] = []
        row_total: str = "Total "
        for key in self.keys:
            row_total = f"{row_total} & {self.total_results.get()[key][header_key]:.2f}"
        rows.append(f"{row_total} \\\\")

        for card, result in self.cardinality_results.items():
            row: str = f"{card} "
            for key in self.keys:
                row = f"{row} & {result.get()[key][header_key]:.2f}"
            rows.append(f"{row} \\\\")

        return rows

    def results_for_calculation(self, header_key: str):
        rows: List[List[Union[str, float]]] = []
        for relation, result in self.relation_results.items():
            row: List[Union[str, float]] = [relation]
            for key in self.keys:
                row.append(result.get()[key][header_key])
            rows.append(row)

        rows = sorted(rows, key=lambda row: row[0])
        return [["relations"] + self.keys] + rows

    def results_for_persistence(self, header_key: str
                                ) -> List[Tuple[str, str | None, float]]:
        rows: List[Tuple[str, str | None, float]] = []
        for key, res in self.total_results.get().items():
            rows.append((key, None, res[header_key]))
        for card in self.cardinality_results.keys():
            for key, res in self.cardinality_results[card].get().items():
                rows.append((key, card, res[header_key]))
        for relation, result in self.relation_results.items():
            for key in self.keys:
                rows.append((key, relation, result.get()[key][header_key]))
        return rows


