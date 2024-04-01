#!/usr/bin/python3
'''api status'''
from models.base_model import State, User, Amenity, City, Place, Review
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def return_status():
    '''return status'''
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def return_stats():
    '''JSON Responses'''
    todos = {
        'states': State, 'users': User,
        'amenities': Amenity, 'cities': City,
        'places': Place, 'reviews': Review
    }
    for key, model in todos.items():
        todos[key] = storage.count(model)
    return jsonify(todos)


if __name__ == "__main__":
    app_views.run(host='0.0.0.0', port=5000)

