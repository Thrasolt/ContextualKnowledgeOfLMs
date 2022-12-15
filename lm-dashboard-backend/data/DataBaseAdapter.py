from abc import ABC

import mysql.connector


class DataBaseAdapter(ABC):
    def __init__(self):
        self.connection = mysql.connector.connect(
            user='root',
            password='password',
            host='127.0.0.1',
            database='syntaxComparison')

    def close(self):
        self.connection.close()


