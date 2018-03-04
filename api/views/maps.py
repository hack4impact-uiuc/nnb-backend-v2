from api import app
from flask import Blueprint, request
from api import db
from api.models import Map
import json
from flask import jsonify
#from api.utils import InvalidUsage
from sqlalchemy import func
# import time
# from datetime import date
# import uuid
from flask_sqlalchemy import SQLAlchemy
from api.utils import create_response



mod = Blueprint('maps', __name__)


#none of these have been comprehsnsively tested yet

@app.route('/maps', methods = ['GET'])
# Get all map years.
# get function is definitely not functional
def get_map_years():
    if request.method == 'GET':
        data_in = to_dict(Map.query.all())
        year_list = []
        for k in data_in.keys():
            year_list.append(data_in[k].map_year)
        return create_response(data = year_list)


@app.route('/maps', methods = ['POST'])
# Post a Map
def create_map():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return create_response(status = 400, message = 'failed to enter any data')
# do I have to worry any (None) data
        map_year = data.get('map_year')
        image_url = data.get('image_url')
        if image_url is None:
            return create_response(status = 400, message = 'no image_url entered')
        if map_year is None:
            return create_response(status = 400, message = 'no map_year entered')
        # original code implementation -> data_in = Maps(
        #    image_url = (json_dict['image_url']),
        #    map_year = (int)(json_dict['year'])
        #)
        data_in = Map(
            image_url = image_url,
            map_year = map_year
        )
        # original code has a db.session.commit(), why are we committing?
        db.session.add(data_in)
        db.session.commit()
        return create_response(data_in, message = 'Post successful')

@app.route('/maps/<map_id>', methods = ['DELETE'])
def delete_map(map_id):
    map_obj = Map.query.get(map_id)
    if map_obj is None:
        return create_response(status = 404, message = "ID not found")
    else:
        db.session.delete(map_obj)
        db.session.commit()
        return create_response(status = 200, message = 'Map delete successful')

    # data_list_id = filter(lambda x: x.id, Map.query.all())
    # if map_id not in data_list_id:
    #     return create_response(status = 402, message = 'ID not Found')
    # else:
    #     db.session.delete(map_to_delete)
    #     db.session.commit()
    #     return create_response(status = 200, message= 'Delete succesful')
