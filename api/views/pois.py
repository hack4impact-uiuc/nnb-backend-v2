from api import app
from flask import Blueprint, request, jsonify
from api.models import POI
import json
from api.utils import create_response, InvalidUsage

mod = Blueprint('POIS', __name__)

@app.route('/pois', methods=['GET'])
def pois_get_by_map_year_or_story():
    map_year = request.args.get('map_year')
    story_id = request.args.get('story_id')
    if map_year is not None and story_id is None:
        #find pois by map year
    elif story_id is not None and map_year is None:
        #find pois by story_id
    return create_response(data)

@app.route('/pois/<poi_id>', methods=['GET'])
def pois_get_by_id(poi_id):
    return create_response(data)

@app.route('/pois', methods=['POST'])
def pois_post():
    data = request.get_json()
    return create_response(data)

@app.route('/pois/<poi_id>', methods=['PUT'])
def pois_put(poi_id):
    data = request.get_json()
    return create_response(data)

@app.route('/pois/<poi_id>', methods=['DELETE'])
def pois_delete(poi_id):
    return create_response(data)