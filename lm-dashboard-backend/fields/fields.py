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

comparison_field: Dict = {
    'id': fields.Integer,
    'model': fields.String,
    'metric': fields.String,
    'left_sentence': fields.String,
    'right_sentence': fields.String,
    'relation': fields.String,
    'subject': fields.String,
    'object': fields.String,
    'value': fields.Float,
}

global_comparison_field: Dict = {
    'left_sentence': fields.String,
    'right_sentence': fields.String,
    'value': fields.Float,
}

comparison_list_field = {
    "data": fields.List(fields.Nested(comparison_field))
}

global_comparison_list_field = {
    "data": fields.List(fields.Nested(global_comparison_field))
}
