#!/usr/bin/python3
"""City view object that hanldes all default RESTFUL api"""

from flask import abort, make_response, jsonify, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)  # noqa
def city_state(state_id):
    """retrives all city objects of a state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object from storage"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)  # noqa
def create_city(state_id):
    """creates a new city object"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, 'Not a JSON')
    if "name" not in new_city:
        abort(400, 'Missing name')
    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def delete(city_id):
    """delete city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)  # noqa
def update_city(city_id):
    """updates a city by city_id"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
