from api import app, db
from flask import Blueprint, request, jsonify
from api.models import Map
import json
#from api.utils import InvalidUsage
from sqlalchemy import func
# import time
# from datetime import date
# import uuid
from flask_sqlalchemy import SQLAlchemy
from api.utils import create_response, row_constructor



mod = Blueprint('maps', __name__)

#none of these have been comprehsnsively tested yet

@app.route('/maps', methods = ['GET'])
# Get all map years.
# get function is definitely not functional
def get_map_years():
    data_in = to_dict(Map.query.all())
	year_list = []
	for k in data_in.keys():
	    year_list.append(data_in[k].map_year)
    return create_response(data = year_list)

@app.route('/maps', methods = ['POST'])
# Post a Map
def create_map():
    data = request.get_json()
    if data is None:
        return create_response(status = 400, message = 'failed to enter any data')
    map_year = data.get('map_year')
    image_url = data.get('image_url')
    if image_url is None:
        return create_response(status = 400, message = 'no image_url entered')
    if map_year is None:
        return create_response(status = 400, message = 'no map_year entered')
    # original code implementation -> created_map = Maps(
    #    image_url = (json_dict['image_url']),
    #    map_year = (int)(json_dict['year'])
    #)
    created_map = row_constructor(image_url, map_year)
    db.session.add(created_map)
    db.session.commit()
    return create_response(created_map, message = 'Post successful')

@app.route('/maps/<map_id>', methods = ['DELETE'])
def delete_map(map_id):
    map_obj = Map.query.get(map_id)
    if map_obj is None:
        return create_response(status = 404, message = 'ID not found')
    else:
        db.session.delete(map_obj)
        db.session.commit()
        return create_response(status = 200, message = 'Map delete successful')

    # data_list_id = filter(lambda x: x.id, Map.query.all())
    # if map_id not in data_list_id:
    #     return create_response(status = 402, message = 'ID not Found')
