import json
from os import curdir, path

from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


class Results(Resource):
    def get(self, site_name):
        with open(path.join(curdir, 'results', '%s.json' % site_name), 'r') as f:
            return json.loads(f.read())


api.add_resource(Results, '/<string:site_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=443,
            ssl_context=('/etc/letsencrypt/live/webaccessibility.rocks/fullchain.pem',
                         '/etc/letsencrypt/live/webaccessibility.rocks/privkey.pem'))
