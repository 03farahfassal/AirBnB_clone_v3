#!/usr/bin/python3
"""
A view for the Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_city(city_id):
    """retrieve places based on city_id"""

    if request.method == 'GET':
        city = storage.get(City, city_id)

        if city:
            places = [place.to_dict() for place in city.places]
            return jsonify(places)
        abort(404)
    elif request.method == 'POST':
        city = storage.get(City, city_id)

        if city:
            my_dict = request.get_json()
            if not my_dict:
                abort(400, 'Not a JSON')
            if 'user_id' not in my_dict:
                abort(400, 'Missing user_id')
            if 'name' not in my_dict:
                abort(400, 'Missing name')
            user_id = my_dict['user_id']
            user = storage.get(User, user_id)

            if user:
                place = Place(**my_dict)
                place.city_id = city_id
                place.save()
                return jsonify(place.to_dict()), 201
            abort(404)
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_by_place_id(place_id):
    """Retrieves a place based on the place_id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        for k, v in my_dict.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
