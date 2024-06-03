#!/usr/bin/python3
"""Place object RESTFul API actions"""

from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)  # noqa
def get_reviews_by_place(place_id):
    """Retrieves the list of all reviews"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)  # noqa
def get_review(review_id):
    """get review by review id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def delete_review(review_id):
    """delete review based on review id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}),  200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)  # noqa
def create_review(place_id):
    """creates a review for place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get("User", data["user_id"])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    review = Review(**data)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)  # noqa
def update_review(review_id):
    """update the review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:  # noqa
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
