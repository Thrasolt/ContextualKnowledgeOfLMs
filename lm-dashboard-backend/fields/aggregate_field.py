from typing import Dict
from flask_restful import fields


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