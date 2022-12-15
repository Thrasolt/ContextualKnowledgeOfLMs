from typing import List

from .DataBaseAdapter import DataBaseAdapter


class Score:
    def __init__(self, id: int, model: str, sentence: str, relation: str,
                 subj: str, obj: str, score: float):
        self.id = id
        self.model = model
        self.sentence = sentence
        self.relation = relation
        self.subj = subj
        self.subj = obj
        self.score = score


class ScoreAdapter(DataBaseAdapter):

    def __init__(self):
        super().__init__()

    def get_scores(self, model_name: str) -> List:
        query: str = "SELECT * FROM scores WHERE model = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, [model_name])
        return list(map(
            lambda row: Score(*row),
            cursor.fetchall()))
