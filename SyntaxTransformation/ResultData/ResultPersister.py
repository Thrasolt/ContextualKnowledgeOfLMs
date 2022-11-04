from __future__ import annotations

import mysql.connector
from typing import List, Tuple

TABLE_NAME: str = "Results"

DATABASE_PATH: str = '/Users/tim/projects/ContextualKnowledgeOfLMs/SyntaxTransformation/ResultData/result.db'


class ResultPersister:
    def __init__(self, model: str, measure: str, data_source: str, table_name: str = TABLE_NAME):
        self.model: str = model
        self.measure: str = measure
        self.data_source: str = data_source
        self.table_name: str = table_name
        self.connection = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='syntaxComparison')

    def check_for_row(self, sentence: str, filter_name: str) -> int | None:
        operator: str = f"SELECT * FROM {self.table_name}"
        condition: str = f"WHERE model='{self.model}' AND data='{self.data_source}' AND measure='{self.measure}' " \
                         f"AND filter='{filter_name}' AND sentence='{sentence}'"
        statement: str = f"{operator} {condition}"

        cursor = self.connection.cursor(prepared=True)
        cursor.execute(statement)

        results: List = cursor.fetchall()

        if len(results) > 0:
            row_id: int = int(results[0][0])
            return row_id
        return None

    def update_row(self, row_id: int, value: float):
        operator: str = f"UPDATE {self.table_name} SET value={value}"
        condition: str = f"WHERE id={row_id} "
        statement: str = f"{operator} {condition}"

        cursor = self.connection.cursor(prepared=True)
        cursor.execute(statement)

    def save_row(self, sentence: str, value: float):
        operator: str = f"INSERT INTO {self.table_name}"
        rows: str = f"(model, data, measure, sentence, value) VALUES (%s, %s, %s, %s, %s)"
        values: Tuple = (self.model, self.data_source, self.measure, sentence, value)
        statement: str = f"{operator} {rows}"

        cursor = self.connection.cursor(prepared=True)
        cursor.execute(statement, values)

    def save_row_filter(self, sentence: str, filter_name: str, value: float):
        operator: str = f"INSERT INTO {self.table_name}"
        rows: str = f"(model, data, measure, sentence, filter, value) VALUES (%s, %s, %s, %s, %s, %s)"
        values: Tuple = (self.model, self.data_source, self.measure, sentence, filter_name, value)
        statement: str = f"{operator} {rows}"

        cursor = self.connection.cursor(prepared=True)
        cursor.execute(statement, values)

    def persist_row(self, sentence: str, filter_name: str, value: float):
        row_id: int = self.check_for_row(sentence, filter_name)
        if row_id is None:
            if filter_name is None:
                self.save_row(sentence, value)
            else:
                self.save_row_filter(sentence, filter_name, value)
        else:
            self.update_row(row_id, value)

    def persist(self, rows: List[Tuple[str, str, str, str, str | None, float]]):
        for row in rows:
            self.persist_row(*row)

    def close(self):
        self.connection.commit()
        self.connection.close()


