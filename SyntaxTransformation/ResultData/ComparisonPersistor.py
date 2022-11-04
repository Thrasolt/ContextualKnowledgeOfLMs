from typing import List

from .BasePersistor import Persistor

TABLE_NAME: str = "Comparisons"


class ComparisonPersistor(Persistor):

    def __init__(self, model: str, metric: str):
        super().__init__()
        self.model: str = model
        self.metric: str = metric
        self.table_name = TABLE_NAME

    def build_search_query(self) -> str:
        return f"""
            SELECT id FROM {self.table_name} 
            WHERE model = %s AND metric = %s
            AND left_sentence = %s AND right_sentence = %s
            AND relation =  %s AND subject = %s AND object = %s; 
            """

    def build_insert_query(self) -> str:
        return f"""
            INSERT INTO {self.table_name} (model, metric, left_sentence, right_sentence, relation, subject, object, value)
            values(%s,  %s, %s,  %s,  %s,  %s,  %s, %s);
            """

    def build_replace_query(self) -> str:
        return f"""
            REPLACE INTO {self.table_name} (model, metric, left_sentence, right_sentence, relation, subject, object, value)
            values(%s,  %s, %s,  %s,  %s,  %s,  %s, %s);
            """

    def build_update_query(self):
        return f"""
            UPDATE {self.table_name} SET value = %s
            WHERE id = %s;
            """

    def check_for_row(self,
                      left_sentence: str, right_sentence: str,
                      rel: str, subj: str, obj):
        query: str = self.build_search_query()
        parameters: List = [self.model, self.metric, left_sentence, right_sentence, rel, subj, obj]
        results: List = self.execute_query(query, parameters)

        if len(results) > 0:
            row_id: int = int(results[0][0])
            return row_id
        return None

    def save_row(self, left_sentence: str, right_sentence: str,
                 rel: str, subj: str, obj: str, value: float):
        query: str = self.build_insert_query()
        parameters: List = [self.model, self.metric, left_sentence, right_sentence, rel, subj, obj, value]
        self.execute_update(query, parameters)

    def update_row(self, row_id: int, value: float):
        query: str = self.build_update_query()
        parameters: List = [value, row_id]
        self.execute_query(query, parameters)

    def persist_row(self, left_sentence: str, right_sentence: str,
                    rel: str, subj: str, obj: str, value: float):
        row_id: int = self.check_for_row(left_sentence, right_sentence, rel, subj, obj)
        if row_id is None:
            self.save_row(left_sentence, right_sentence, rel, subj, obj, value)
        else:
            self.update_row(row_id, value)
        self.update_statement_counter()

    def persist_row_fast(self, left_sentence: str, right_sentence: str,
                    rel: str, subj: str, obj: str, value: float):
        query: str = self.build_replace_query()
        parameters: List = [self.model, self.metric, left_sentence, right_sentence, rel, subj, obj, value]
        self.execute_update(query, parameters)
