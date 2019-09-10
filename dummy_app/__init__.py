from dummy_app import shelve_db

from flask import Flask
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

store = shelve_db.ShelveDb('incense-sticks.db')


@app.teardown_appcontext
def teardown_db(exception):
    store.teardown_db(exception)

@app.route("/health")
def health():
    """For monitoring the service"""

    return '', 200

class IncenseSticks(Resource):
    def get(self):
        incenseSticks = store.get_all()

        return {'items': incenseSticks}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('manufacturer', required=True)
        parser.add_argument('number-of-sticks', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        store.upsert(args['identifier'], args)

        return args, 201

class IncenseStick(Resource):
    def get(self, identifier):
        try:
            item = store.get_one(identifier)
        except Exception:
            # If the key does not exist in the data store, return a 404 error.
            return '', 404

        return item, 200

    def delete(self, identifier):
        try:
            store.delete(identifier)
        except Exception:
            # If the key does not exist in the data store, return a 404 error.
            return '', 404

        return '', 204

api.add_resource(IncenseSticks, '/incense-sticks')
api.add_resource(IncenseStick, '/incense-stick/<string:identifier>')
