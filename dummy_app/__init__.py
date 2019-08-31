from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

@app.route("/health")
def health():
    """For monitoring the service"""

    return '', 200

