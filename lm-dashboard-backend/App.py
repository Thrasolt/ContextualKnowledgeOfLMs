from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from ScoreController import ScoreController
from AggregateVerbController import AggregateVerbController
from AggregateController import AggregateController
from GlobalFeatureComparisonController import GlobalFeatureComparisonController

app = Flask(__name__)
api = Api(app)
CORS(app)


api.add_resource(ScoreController, "/scores/<string:model_name>")
api.add_resource(AggregateController, "/aggregate/")
api.add_resource(AggregateVerbController, "/aggregate/verb/<string:model_name>")
api.add_resource(GlobalFeatureComparisonController, "/comparison")

if __name__ == '__main__':
    app.run(debug=True)
