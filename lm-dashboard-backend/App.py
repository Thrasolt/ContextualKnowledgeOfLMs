from typing import Dict

from flask import Flask
from flask_restful import Resource, Api, fields
from flask_cors import CORS

from ScoreController import ScoreController

app = Flask(__name__)
api = Api(app)
CORS(app)


api.add_resource(ScoreController, "/scores/<string:model_name>")

if __name__ == '__main__':
    app.run(debug=True)