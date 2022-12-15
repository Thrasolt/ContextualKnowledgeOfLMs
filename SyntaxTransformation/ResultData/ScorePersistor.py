from __future__ import annotations

from typing import Tuple, List

from .ResultPersister import ResultPersister

TABLE_NAME: str = "Scores"

ScoreRow = List[Tuple[str, str, str, str, float]]


class ScorePersistor(ResultPersister):

    def __init__(self, model: str, table_name: str = TABLE_NAME):
        super().__init__(model, "score", "complete", table_name)
        self.statement_counter: int = 0

    def persist(self, rows: ScoreRow):
        for row in rows:
            self.persist_score_row(*row)

    def build_search_query(self) -> str:
        return f"""
            SELECT id FROM {self.table_name} 
            WHERE model = %s AND sentence = %s AND relation=  %s 
            AND subject = %s AND object= %s ; 
            """

    def build_insert_query(self) -> str:
        return f"""
            INSERT INTO {self.table_name} (model, sentence, relation, subject, object, score)
            values( %s ,  %s ,  %s ,  %s ,  %s ,  %s );
            """

    def build_update_query(self):
        return f"""
            UPDATE {self.table_name} SET score = %s
            WHERE model= %s AND sentence=  %s 
            AND subject= %s AND object= %s AND relation= %s; 
            """

    def execute_query(self, query: str, params: List[str]) -> List:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def check_for_score_row(self, sentence: str, rel: str, subj: str, obj: str) -> int | None:
        query: str = self.build_search_query()
        results: List = self.execute_query(query, [self.model, sentence, rel, subj, obj])

        if len(results) > 0:
            row_id: int = int(results[0][0])
            return row_id
        return None

    def persist_score_row(self, sentence: str, rel: str, subj: str, obj: str, score: float):
        row_id: int = self.check_for_score_row(sentence, rel, subj, obj)
        if row_id is None:
            self.save_score_row(sentence, rel, subj, obj, score)
        else:
            self.update_score_row(sentence, rel, subj, obj, score)
        self.update_statement_counter()

    def save_score_row(self, sentence: str, rel: str, subj: str, obj: str, score: float):
        query: str = self.build_insert_query()
        self.execute_query(query, [self.model, sentence, rel, subj, obj, score])

    def update_score_row(self, sentence: str, rel: str, subj: str, obj: str, score: float):
        query: str = self.build_update_query()
        self.execute_query(query, [self.model, score, sentence, rel, subj, obj])

    def update_statement_counter(self):
        self.statement_counter += 1
        if self.statement_counter > 100:
            self.connection.commit()
            self.statement_counter = 0




