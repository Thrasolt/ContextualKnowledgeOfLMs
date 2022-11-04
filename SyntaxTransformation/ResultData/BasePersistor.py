from abc import ABC
from typing import List

import mysql.connector


class Persistor(ABC):
    def __init__(self):
        self.connection = mysql.connector.connect(
            user='root',
            password='password',
            host='127.0.0.1',
            database='syntaxComparison')
        self.statement_counter = 0

    def execute_query(self, query: str, params: List[str]) -> List:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def execute_update(self, query: str, params: List[str]):
        cursor = self.connection.cursor()
        cursor.execute(query, params)

    def update_statement_counter(self):
        self.statement_counter += 1
        if self.statement_counter > 100:
            self.commit()
            self.statement_counter = 0

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.connection.close()




