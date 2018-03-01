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


mod = Blueprint('maps', __name__)

def create_response(data={}, status=200, message=''):
    """
    Wraps response in a consistent format throughout the API
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    """
    response = {
        'success': 200 <= status < 300,
        'code': status,
        'message': message,
        'result': data
    }
    return jsonify(response), status
#none of these have been comprehsnsively tested yet

@app.route('/maps', methods = ['GET', 'POST'])
# Get all map years.
# get function is definitely not functional
def map_():
    if request.method == 'GET':
        print(Map.query.all())
        data_in = Map.query.all()
        data_in = list(filter(lambda x : x.map_year, data_in))
        return create_response(data = data_in)
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return create_response(status = 402, message = 'failed to enter any data')
# do I have to worry any (None) data
        map_year = data.get('map_year')
        image_url = data.get('image_url')
        if image_url is None:
            return create_response(status = 402, message = 'no image_url entered')
        if map_year is None:
            return create_response(status = 402, message = 'no map_year entered')
        # original code implementation -> data_in = Maps(
        #    image_url = (json_dict['image_url']),
        #    map_year = (int)(json_dict['year'])
        #)
        data_in = Map(
            image_url = data.get('image_url'),
            map_year = data.get('map_year')
        )
        # original code has a db.session.commit(), why are we committing?
        db.session.add(data_in)
        db.session.commit()
        return create_response(data, message = 'Post successful')

@app.route('/maps/<map_id>', methods = ['DELETE'])
def delete_map(map_id):
    map_obj = Map.query.get(map_id)
    if map_obj is None:
        return create_response(status = 402, message = "ID not found")
    else:
        db.session.delete(map_obj)
        db.session.commit()
        return create_response(status = 200, message = 'Delete successful')

    # data_list_id = filter(lambda x: x.id, Map.query.all())
    # if map_id not in data_list_id:
    #     return create_response(status = 402, message = 'ID not Found')
    # else:
    #     db.session.delete(map_to_delete)
    #     db.session.commit()
    #     return create_response(status = 200, message= 'Delete succesful')
