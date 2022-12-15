from typing import List

from .DataBaseAdapter import DataBaseAdapter


class ComparisonData:
    def __init__(self, id: int, model: str, metric: str, left_sentence: str, right_sentence: str,
                 relation: str, subject: str, obj: str, value: float):
        self.id = id
        self.model = model
        self.metric = metric
        self.left_sentence = left_sentence
        self.right_sentence = right_sentence
        self.relation = relation
        self.subject = subject
        self.object = obj
        self.value = value


class GlobalComparisonData:
    def __init__(self, left_sentence: str, right_sentence: str, value: float):
        self.left_sentence = left_sentence
        self.right_sentence = right_sentence
        self.value = value


class ComparisonAdapter(DataBaseAdapter):

    def __init__(self):
        super().__init__()

    def get_comparison_data(self, model_name: str, metric: str) -> List[ComparisonData]:
        query: str = "SELECT * FROM Comparisons WHERE model = %s AND metric like %s"
        params: List[str] = [model_name, f"%{metric}%"]
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return list(map(
            lambda row: ComparisonData(*row),
            cursor.fetchall()))

    def get_global_comparison_data(self, model_name: str, metric: str) -> List[GlobalComparisonData]:
        query: str = """
            select left_sentence, right_sentence, avg(value) from Comparisons
                        where model = %s and metric like %s
                        group by left_sentence, right_sentence, right_sentence;
            """
        params: List[str] = [model_name, f"%{metric}%"]
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return list(map(
            lambda row: GlobalComparisonData(*row),
            cursor.fetchall()))

    def get_global_comparison_data_for_verbs(self, model_name: str, metric: str) -> List[GlobalComparisonData]:
        query: str = """
            select left_sentence, right_sentence, avg(value) from Comparisons
                        where model = %s and metric like %s and relation in ('P127', 'P136', 'P176', 'P178', 'P413', 'P1303')
                        group by left_sentence, right_sentence, right_sentence;
            """
        params: List[str] = [model_name, f"%{metric}%"]
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return list(map(
            lambda row: GlobalComparisonData(*row),
            cursor.fetchall()))
