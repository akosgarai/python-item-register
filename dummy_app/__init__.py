import shelve

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("incense-sticks.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/health")
def health():
    """For monitoring the service"""

    return '', 200

class IncenseSticks(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        incenseSticks = []

        for key in keys:
            incenseSticks.append(shelf[key])

        return {'items': incenseSticks}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('manufacturer', required=True)
        parser.add_argument('number-of-sticks', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        return args, 201

class IncenseStick(Resource):
    def get(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return '', 404

        return shelf[identifier], 200

    def delete(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return '', 404

        del shelf[identifier]
        return '', 204

api.add_resource(IncenseSticks, '/incense-sticks')
api.add_resource(IncenseStick, '/incense-stick/<string:identifier>')
