from typing import Dict

from flask_restful import Resource, marshal_with, reqparse
from fields.fields import global_comparison_list_field
from data.ComparisonAdapter import ComparisonAdapter

class GlobalFeatureComparisonController(Resource):

    @marshal_with(global_comparison_list_field)
    def post(self) -> Dict:

        adapter = ComparisonAdapter()

        parser = reqparse.RequestParser()
        parser.add_argument('model_name', type=str, required=True)
        parser.add_argument('metric', type=str, required=True)
        parser.add_argument('nominalized', type=str, required=False)
        args = parser.parse_args()

        model_name: str = args['model_name']
        metric: str = args['metric']

        try:
            if 'nominalized' in args.keys():
                query_results = adapter.get_global_comparison_data_for_verbs(model_name, metric)
            else:
                query_results = adapter.get_global_comparison_data(model_name, metric)
        except Exception as exception:
            print(exception)
            query_results = []

        adapter.close()
        return {"data": query_results}
