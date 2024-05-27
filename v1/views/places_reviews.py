#!/usr/bin/python3
"""Places reviews view module"""
from models import storage
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/places/<place_id>/reviews')
def get_reviews(place_id):
    """Get reviews for a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    return [review.to_dict() for review in place.reviews]


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """Get a review by id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    return review.to_dict()


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new review"""
    from models.review import Review

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    if 'user_id' not in payload:
        abort(400, 'Missing user_id')

    user_id = payload['user_id']
    if storage.get("User", user_id) is None:
        abort(404)

    if 'text' not in payload:
        abort(400, 'Missing text')

    review = Review(**payload)
    review.place_id = place_id
    review.save()

    return review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    try:
        payload = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    for key, value in payload.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue
        setattr(review, key, value)

    review.save()
    return review.to_dict()


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    review.delete()
    return jsonify({}), 200
