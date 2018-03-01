from api import app, db
from api.models import Story, StoryPOI
from api.utils import create_response, InvalidUsage
from sqlalchemy.sql.expression import func
from flask import Blueprint, request, jsonify
import json
from datetime import date
from dateutil.parser import parse

mod = Blueprint('stories', __name__)

STORIES = "/stories"
STORIES_PARAM = "/stories/<story_id>"

@app.route(STORIES, methods=['GET'])
def get_stories():
    if 'POI' in request.args:
        stories = StoryPOI.query.filter(StoryPOI.poi_id == request.args.get('POI'))
        if stories.count() == 0:
            return create_response(status=404, message='No stories found for specified POI')
        else:
            return create_response({'stories':stories})
    else:
        return create_response({'stories':Story.query.all()})

@app.route(STORIES, methods=['PUT'])
def put_stories():
    data = request.get_json()
