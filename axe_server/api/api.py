import json
import sqlite3 as sql
from os import curdir, path

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource

DATABASE = path.join(curdir, 'axe_server', 'db', 'site_data.db')

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


class Results(Resource):
    def get(self, site_name):
        with sql.connect(DATABASE) as db:
            c = db.cursor()
            query = """
                SELECT * FROM data WHERE name = \"{}\" ORDER BY updated
                """.format(site_name)
            c.execute(query)
            row = c.fetchall()
            data = {
                "last_updated": row[0][2],
                "violations": json.loads(row[0][3])
            }
        return data


api.add_resource(Results, '/<string:site_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=443,
            ssl_context=('/etc/letsencrypt/live/webaccessibility.rocks/fullchain.pem',
                         '/etc/letsencrypt/live/webaccessibility.rocks/privkey.pem'))
