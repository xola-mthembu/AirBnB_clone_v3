#!/usr/bin/python3
"""
Review view for handling all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    user = storage.get("User", request.json['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.json:
        abort(400, description="Missing text")
    data = request.get_json()
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
