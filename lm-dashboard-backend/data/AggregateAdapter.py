from .DataBaseAdapter import DataBaseAdapter

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"
TYPOLOGY_SENTENCES = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

ACTIVE = "active"
PASSIVE = "passive"
NOMINAL = "nominalized"

TYPOLOGY_VERB = [ACTIVE, PASSIVE, NOMINAL]

class AggregateData:
    def __init__(self, id: int, model: str, measure: str, data: str, sentence: str,
                 filterName: str, value: float):
        self.id = id
        self.model = model
        self.measure = measure
        self.data = data
        self.sentence = sentence
        self.filterName = filterName
        self.value = value


class AggregateAdapter(DataBaseAdapter):

    def __init__(self):
        super().__init__()

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

    def get_data(self):
        query: str = "SELECT id, model, measure, data, sentence, filter as filterName, value FROM Results"
        cursor = self.connection.cursor()
        cursor.execute(query)
        return list(map(
            lambda row: AggregateData(*row),
            cursor.fetchall()))

