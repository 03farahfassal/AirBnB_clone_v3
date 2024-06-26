#!/usr/bin/python3

"""Handles all restful actions for reviews"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models import storage
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews_by_place(place_id):
    """retrieve reviews based on place_id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    elif request.method == 'POST':
        my_dict = request.get_json()

        if my_dict is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in my_dict:
            abort(400, 'Missing user_id')
        if 'text' not in my_dict:
            abort(400, 'Missing text')
        user_id = data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        review = Review(**my_dict)
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_by_review_id(review_id):
    """retrieves review by review id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        my_dict = request.get_json()
        if not my_dict:
            abort(400, 'Not a JSON')
        for k, v in my_dict.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
