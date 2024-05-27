#!/usr/bin/python3
"""Places view module"""
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places")
def city_places(city_id):
    """Returns a list of places of a specific City"""

    city = storage.get("City", city_id)

    if not city:
        abort(404)

    places_list = [place.to_dict() for place in city.places]

    return jsonify(places_list), 200


@app_views.route("/places/<place_id>")
def get_place(place_id):
    """Return a place by its id"""

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates a new place that is a part of a specific city"""
    from models.place import Place

    city = storage.get('City', city_id)

    if not city:
        abort(404)

    try:
        place_data = request.get_json()
        if not place_data:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    if 'user_id' not in place_data:
        abort(400, description="Missing user_id")

    user = storage.get('User', place_data['user_id'])

    if not user:
        abort(404)

    if 'name' not in place_data:
        abort(400, description="Missing name")

    new_place = Place(**place_data)
    new_place.city_id = city_id

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a place"""

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    try:
        new_data = request.get_json()
        if new_data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a place using its id"""

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


# @app_views.route('/cities/<city_id>/places')
# def get_places(city_id):
#     """Get all places"""
#     city = storage.get("City", city_id)
#     if city is None:
#         abort(404)

#     return [place.to_dict() for place in city.places]


# @app_views.route('/places/<place_id>')
# def get_place(place_id):
#     """Get a place by id"""
#     place = storage.get("Place", place_id)
#     if place is None:
#         abort(404)

#     return place.to_dict()


# @app_views.route('/cities/<city_id>/places', methods=['POST'])
# def create_place(city_id):
#     """Creates a place object"""
#     from models.place import Place

#     city = storage.get("City", city_id)
#     if city is None:
#         abort(404)

#     try:
#         payload = request.get_json()
#         if not payload:
#             abort(400, description="Not a JSON")
#     except Exception as e:
#         abort(400, description="Not a JSON")

#     if "user_id" not in payload:
#         abort(400, "Missing user_id")

#     user_id = payload["user_id"]
#     user = storage.get("User", user_id)
#     if user is None:
#         abort(404)

#     if "name" not in payload:
#         abort(400, "Missing name")

#     place = Place(**payload)
#     place.city_id = city_id
#     place.save()
#     return (place.to_dict(), 201)


# @app_views.route('/places/<place_id>', methods=['PUT'])
# def update_place(place_id):
#     """Updates a place object"""
#     place = storage.get("Place", place_id)
#     if place is None:
#         abort(404)

#     try:
#         payload = request.get_json()
#     except Exception:
#         abort(400, 'Not a JSON')

#     for key, value in payload.items():
#         if key in ("id", "user_id", "city_id", "created", "updated_at"):
#             continue
#         setattr(place, key, value)

#     place.save()
#     return (place.to_dict(), 200)


# @app_views.route('/places/<place_id>', methods=['DELETE'])
# def delete_place(place_id):
#     """Deletes a place object by id"""
#     place = storage.get("Place", place_id)
#     if place is None:
#         abort(404)

#     place.delete()
#     return jsonify({}), 200
