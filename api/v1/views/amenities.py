#!/usr/bin/python3
"""creates a view for Amenity objects that handle all
    default RESTFul API actions
"""
from flask import jsonify, request, make_response, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)  # noqa
def get_amenity():
    """retrieves the list of ameninty objects from storage"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)  # noqa
def ameninty_by_id(amenity_id):
    """retrieves a single amentity by id"""
    ameninty = storage.get("Amenity", amenity_id)
    if ameninty is None:
        abort(404)
    return jsonify(ameninty.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def delete_amenity(amenity_id):
    """deletes an amenity"""
    ameninty = storage.get("Amenity", amenity_id)
    if ameninty is None:
        abort(404)
    ameninty.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates amenity object"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if 'name' not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)  # noqa
def update_amenity(amenity_id):
    """updates existing amenity"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    for key, value in new_amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
