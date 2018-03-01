from api import app, db
from api.models import POI, Media, Link, Story, StoryPOI
from api.utils import create_response, InvalidUsage
from sqlalchemy.sql.expression import func
from flask import Blueprint, request, jsonify
import json
from datetime import date
from dateutil.parser import parse

mod = Blueprint('stories', __name__)

GET_STORIES = "/stories"

# @app.route(GET_STORIES, methods=['GET'])
# def get_stories():
#     if 'POI' in request.args:
#         stories = STORY_POI.query.filter(STORY_POI.poi_id == request.args.get('POI'))
#         if stories.count() == 0:
#             return create_response(status=404, message='No stories found for specified POI')
#         else return create_response(stories)
#     else:
#         return create_response(STORY.query)
