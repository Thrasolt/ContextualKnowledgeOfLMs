from typing import Dict

from flask_restful import Resource, marshal_with
from fields.fields import score_list_fields
from data.ScoreAdapter import ScoreAdapter


adapter = ScoreAdapter()


class ScoreController(Resource):

    @marshal_with(score_list_fields)
    def get(self, model_name: str) -> Dict:
        query_result = adapter.get_scores(model_name)
        return {"scores": query_result}
