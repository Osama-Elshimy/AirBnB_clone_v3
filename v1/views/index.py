#!/usr/bin/python3
"""The main module for the HBnB API"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns the status of an API"""

    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def stats():
    """Return the number of each objects by type"""
    from models import storage

    classes = {
        "users": "User",
        "cities": "City",
        "places": "Place",
        "states": "State",
        "reviews": "Review",
        "amenities": "Amenity",
    }

    return {key: storage.count(value) for key, value in classes.items()}
