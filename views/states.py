#!/usr/bin/python3
"""States view module"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states')
def get_states():
    """Get all states"""
    states = storage.all("State").values()
    return [state.to_dict() for state in states]


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """Get a state by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    return state.to_dict()


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a state object"""
    from models.state import State

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    if "name" not in payload:
        abort(400, "Missing name")

    state = State(**payload)
    state.save()
    return (state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    for key, value in payload.items():
        if key in ("id", "created_at", "updated_at"):
            continue
        setattr(state, key, value)
    state.save()
    return (state.to_dict(), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state object by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    return jsonify({}), 200
