from api import app, db
from api.models import Map, POI
from api.utils import create_response, row_constructor
from flask import Blueprint, request, jsonify
import json
#from api.utils import InvalidUsage
# from sqlalchemy import func
# import time
# from datetime import date
# import uuid
# from flask_sqlalchemy import SQLAlchemy

MAPS_URL = '/maps'
MAPS_ID_URL = '/maps/<int:map_id>'

mod = Blueprint('maps', __name__)

#none of these have been comprehsnsively tested yet

# Get all maps.
@app.route(MAPS_URL, methods = ['GET'])
def get_map_years():
    maps = [m.to_dict() for m in Map.query.all()]
    return create_response({'maps' : maps})

# Post a Map
@app.route(MAPS_URL, methods = ['POST'])
def create_map():
    data = request.get_json()
    fields = ['image_url', 'map_year']
    map_info = [data.get(field) for field in fields]
    if None in map_info:
        missing_params = filter(lambda x: data.get(x) == None, fields)
        message = 'Missing parameters ' + ', '.join(missing_params)
        return create_response(data, 400, message)
    else:
        created_map = row_constructor(Map, data)
        db.session.add(created_map)
        db.session.flush()
        map_id = created_map.id
        db.session.commit()
        return create_response({'map' : Map.query.get(map_id).to_dict()}, 201, 'Map created')

# delete map and all associated POIs
@app.route(MAPS_ID_URL, methods = ['DELETE'])
def delete_map(map_id):
    map_obj = Map.query.get(map_id)
    if map_obj is None:
        return create_response(status = 404, message = 'Map id ' + str(map_id) + ' not found')
    else:
        poi_list = POI.query.filter(POI.map_year == map_obj.map_year)
        for poi in poi_list:
            db.session.delete(poi)
        db.session.delete(map_obj)
        db.session.commit()
        return create_response(status = 200, message = 'Map deleted')
