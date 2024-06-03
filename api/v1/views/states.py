#!/usr/bin/python3
""" view for State objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """returns a list of all state objects"""
    state_obj = storage.all(State)
    return jsonify([obj.to_dict() for obj in state_obj.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_with_id(state_id):
    """returns an object with given id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def delete_state(state_id):
    "Deletes a state object"
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    new_state = request.get_json()
    if new_state is None:
        abort(400, "Not a JSON")
    if 'name' not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state object by ID"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # update the states object attributes based on json data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
