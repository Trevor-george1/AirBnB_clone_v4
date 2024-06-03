#!/usr/bin/python3
"""creates routes and returns a Json response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status_check():
    """creates a status route that shows status AIDEN"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def number_objects():
    """retrieves the no of each object bu type"""
    objects = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
        }
    return jsonify(objects)
