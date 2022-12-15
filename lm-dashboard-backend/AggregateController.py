

from typing import Dict

from flask_restful import Resource, marshal_with
from data.AggregateAdapter import AggregateAdapter
from fields.aggregate_field import aggregate_list_field

adapter = AggregateAdapter()


class AggregateController(Resource):

    @marshal_with(aggregate_list_field)
    def get(self) -> Dict:
        query_result = adapter.get_data()
        return {"data": query_result}