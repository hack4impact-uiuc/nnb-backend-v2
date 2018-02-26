from api import app
from flask import Blueprint, request
from api.models import POI
import json
from flask import jsonify
from api.utils import create_response, InvalidUsage

mod = Blueprint('main', __name__)

# function that is called when you visit /
@app.route('/')
def index():
    return '<h1>Test 1.0!</h1>'

#function that is called when you visit /persons
# @app.route('/persons')
# def name():
#     try:
# 		data = {'persons': Person.query.all()}
#         create_response(data)
#     except Exception as ex:
#         return create_response(data={}, status=400, message=str(ex))