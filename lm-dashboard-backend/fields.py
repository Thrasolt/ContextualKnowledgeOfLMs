from typing import Dict
from flask_restful import fields


score_field: Dict = {
    'id': fields.Integer,
    'model': fields.String,
    'sentence': fields.String,
    'relation': fields.String,
    'subj': fields.String,
    'obj': fields.String,
    'score': fields.Float,
}

score_list_fields = {
    "scores": fields.List(fields.Nested(score_field))
}

aggregate_field: Dict = {
    'id': fields.Integer,
    'model': fields.String,
    'measure': fields.String,
    'data': fields.String,
    'sentence': fields.String,
    'filterName': fields.String,
    'value': fields.Float,
}

aggregate_list_field = {
    "data": fields.List(fields.Nested(aggregate_field))
}