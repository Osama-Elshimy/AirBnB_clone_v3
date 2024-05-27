#!/usr/bin/python3
"""Amenities view module"""
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/amenities')
def get_amenities():
    """Get all amenities"""
    amenities = storage.all("Amenity").values()
    return [amenity.to_dict() for amenity in amenities]


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """Get an amenity by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    return amenity.to_dict()


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an amenity object"""
    from models.amenity import Amenity

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    if "name" not in payload:
        abort(400, "Missing name")

    amenity = Amenity(**payload)
    amenity.save()
    return (amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    for key, value in payload.items():
        if key in ("id", "created_at", "updated_at"):
            continue
        setattr(amenity, key, value)
    amenity.save()
    return (amenity.to_dict(), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    return jsonify({}), 200
