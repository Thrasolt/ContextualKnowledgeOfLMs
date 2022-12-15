from typing import Dict

from flask_restful import Resource, marshal_with
from data.AggregateAdapter import AggregateAdapter
from fields.aggregate_field import aggregate_list_field

adapter = AggregateAdapter()


class AggregateVerbController(Resource):

    @marshal_with(aggregate_list_field)
    def get(self, model_name: str) -> Dict:
        query_result = adapter.get_verb_typology_data(model_name)
        return {"data": query_result}