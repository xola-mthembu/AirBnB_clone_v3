#!/usr/bin/python3
"""
Places view for handling all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    user = storage.get("User", request.json['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending on the JSON in the request body"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []
    
    if not states and not cities and not amenities:
        places = storage.all("Place").values()
    else:
        if states:
            for state_id in states:
                state = storage.get("State", state_id)
                if state:
                    for city in state.cities:
                        places.extend(city.places)
        if cities:
            for city_id in cities:
                city = storage.get("City", city_id)
                if city:
                    places.extend(city.places)
        if amenities:
            places = [place for place in places if all(amenity in place.amenities for amenity in amenities)]

    places = [place.to_dict() for place in places]
    return jsonify(places)
