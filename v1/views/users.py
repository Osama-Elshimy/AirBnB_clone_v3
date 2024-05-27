#!/usr/bin/python3
"""Users view module"""
# from models import storage
# from api.v1.views import app_views
# from flask import request, jsonify, abort

# #!/usr/bin/python3
# """This module handles all default RESTFul APIs for User object"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User
import hashlib


@app_views.route("/users")
def users_list():
    """Returns a list of all User objects in a json representation"""

    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>")
def get_user(user_id):
    """Return a user by its id"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a user using its id"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    user.delete()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """Creates a new user"""

    try:
        user_data = request.get_json()
        if not user_data:
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    if 'email' not in user_data:
        abort(400, "Missing email")
    if 'password' not in user_data:
        abort(400, "Missing password")

    new_user = User(**user_data)

    encoded_password = hashlib.md5(new_user.password.encode()).hexdigest()
    new_user.password = encoded_password

    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a user"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    if 'password' in user:
        encoded_password = hashlib.md5(user.password.encode()).hexdigest()
        user.password = encoded_password

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict())


# @app_views.route('/users')
# def get_users():
#     """Get all users"""
#     users = storage.all("User").values()
#     return [user.to_dict() for user in users]


# @app_views.route('/users/<user_id>')
# def get_user(user_id):
#     """Get a user by id"""
#     user = storage.get("User", user_id)
#     if user is None:
#         abort(404)
#     return jsonify(user.to_dict())


# @app_views.route('/users', methods=['POST'])
# def create_user():
#     """Create a user"""
#     from models.user import User

#     try:
#         payload = request.get_json()
#     except Exception:
#         abort(400, 'Not a JSON')

#     if "email" not in payload:
#         abort(400, "Missing email")
#     if "password" not in payload:
#         abort(400, "Missing password")

#     user = User(**payload)
#     user.save()
#     return (user.to_dict(), 201)


# @app_views.route('/users/<user_id>', methods=['PUT'])
# def update_user(user_id):
#     """Update a user"""
#     user = storage.get("User", user_id)
#     if user is None:
#         abort(404)

#     try:
#         payload = request.get_json()
#     except Exception:
#         abort(400, 'Not a JSON')

#     for key, value in payload.items():
#         if key in ("id", "email", "created_at", "updated_at"):
#             continue
#         setattr(user, key, value)
#     user.save()
#     return (user.to_dict(), 200)


# @app_views.route('/users/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     """Delete a user"""
#     user = storage.get("User", user_id)
#     if user is None:
#         abort(404)
#     user.delete()
#     return jsonify({}), 200
