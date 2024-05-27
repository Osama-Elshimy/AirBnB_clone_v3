#!/usr/bin/python3
"""Cities view module"""
from models import storage
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states/<state_id>/cities')
def get_cities(state_id):
    """Get all cities"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return [city.to_dict() for city in state.cities]


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    """Get a city by id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a city object"""
    from models.city import City

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    if "name" not in payload:
        abort(400, "Missing name")

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    payload["state_id"] = state_id
    city = City(**payload)
    city.save()
    return (city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    for key, value in payload.items():
        if key in ("id", "state_id", "created_at", "updated_at"):
            continue
        setattr(city, key, value)
    city.save()
    return (city.to_dict(), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object by id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city.delete()
    return jsonify({}), 200
