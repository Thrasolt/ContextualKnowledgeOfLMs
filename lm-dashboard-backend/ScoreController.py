from typing import Dict, List

from flask_restful import Resource, marshal_with
from data.DataBaseAdapter import DataBaseAdapter
from fields import score_list_fields


adapter = DataBaseAdapter()


class ScoreController(Resource):

    @marshal_with(score_list_fields)
    def get(self, model_name: str) -> Dict:
        query_result = adapter.get_scores(model_name)
        return {"scores": query_result}
