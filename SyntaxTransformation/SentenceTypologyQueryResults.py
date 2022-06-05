from typing import List, Dict, Tuple, Union
from tabulate import tabulate


SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"


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
        return self.correct_answers/self.total_answers * 100

    def get(self) -> List[Union[int, float]]:
        return [self.correct_answers, self.total_answers, self.accuracy()]

    def set_top_k(self, top_k: int):
        self.top_k = top_k


class TypologyResults:
    def __init__(self, relation: str, top_k: int):
        self.relation: str = relation
        self.top_k: int = top_k
        self.type_1: RelationResult = RelationResult(relation, top_k)
        self.type_2: RelationResult = RelationResult(relation, top_k)
        self.type_3: RelationResult = RelationResult(relation, top_k)
        self.type_4: RelationResult = RelationResult(relation, top_k)

    def process_answers(self, label: str, answers: List[List]):
        self.type_1.process_answer(label, answers[0])
        self.type_2.process_answer(label, answers[1])
        self.type_3.process_answer(label, answers[2])
        self.type_4.process_answer(label, answers[3])

    def print_result(self):
        print("Results Type 1:")
        self.type_1.print_result()
        print("Results Type 2:")
        self.type_2.print_result()
        print("Results Type 3:")
        self.type_3.print_result()
        print("Results Type 4:")
        self.type_4.print_result()

    def get(self) -> List[List[Union[int, float]]]:
        return [
            [SIMPLE, *self.type_1.get()],
            [COMPOUND, *self.type_2.get()],
            [COMPLEX, *self.type_3.get()],
            [COMCOM, *self.type_4.get()],
        ]

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        self.type_1.set_top_k(top_k)
        self.type_3.set_top_k(top_k)
        self.type_3.set_top_k(top_k)
        self.type_4.set_top_k(top_k)


class SentenceTypologyQueryResults:
    def __init__(self, relations: List[str], top_k: int):
        self.top_k = top_k
        self.relations: List[str] = relations
        self.relation_results: Dict[str, TypologyResults] = {}
        for relation in relations:
            self.relation_results[relation] = TypologyResults(relation, self.top_k)

    def process_answers(self, label: str, relation: str, answers: List[List]):
        if relation in self.relation_results.keys():
            self.relation_results[relation].process_answers(label, answers)

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        for res in self.relation_results.values():
            res.set_top_k(top_k)

    def print_result(self):
        headers = ['type', 'correct', 'total', "accuracy"]
        for relation, result in self.relation_results.items():
            print(f"{relation}:")
            table = tabulate(result.get(), headers, tablefmt='orgtbl')
            print(table)



