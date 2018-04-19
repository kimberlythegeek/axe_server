import json
from json import dumps
from os import curdir
from os.path import join

from flask import Flask, request
from flask_jsonpify import jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)

class Results(Resource):
    def get(self, site_name):
        with open(join(curdir, 'results', '%s.json' % site_name), 'r') as f:
            return json.loads(f.read())


api.add_resource(Results, '/<string:site_name>')


if __name__ == '__main__':
    app.run(port=5002)
