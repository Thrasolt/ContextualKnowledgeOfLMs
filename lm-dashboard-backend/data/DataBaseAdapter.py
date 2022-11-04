from typing import List, Dict

import mysql.connector

TYPOLOGY_SENTENCES = "('simple', 'compound', 'complex', 'compound-complex')"
TYPOLOGY_VERB = "('active', 'passive', 'nominalized')"


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


class AggregateData:
    def __init__(self, id: int, model: str, measure: str, data: str, sentence: str, relation: str,
                    filterName: str, value: float):
        self.id = id
        self.model = model
        self.measure = measure
        self.data: data
        self.sentence: sentence
        self.filterName: filterName
        self.value: value


class DataBaseAdapter:
    def __init__(self):
        self.connection = mysql.connector.connect(
            user='root',
            password='password',
            host='127.0.0.1',
            database='syntaxComparison')

    def get_scores(self, model_name: str) -> List:
        query: str = "SELECT * FROM scores WHERE model = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, [model_name])
        return list(map(
            lambda row: Score(*row),
            cursor.fetchall()))

    def get_sentence_typology_data(self, model_name: str):
        query: str = f"SELECT * FROM Results WHERE model = %s AND sentence in {TYPOLOGY_SENTENCES}"
        cursor = self.connection.cursor()
        cursor.execute(query, [model_name])
        return list(map(
            lambda row: AggregateData(*row),
            cursor.fetchall()))

    def get_verb_typology_data(self, model_name: str):
        query: str = f"SELECT * FROM Results WHERE model = %s AND sentence in {TYPOLOGY_VERB}"
        cursor = self.connection.cursor()
        cursor.execute(query, [model_name])
        return list(map(
            lambda row: AggregateData(*row),
            cursor.fetchall()))

