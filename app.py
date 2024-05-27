#!/usr/bin/python3
"""The main module for the HBnB API"""
import os
import flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

HBNB_API_HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
HBNB_API_PORT = int(os.getenv("HBNB_API_PORT", 5000))

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close the current SQLAlchemy session."""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Return a custom 404 error."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
