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
        stories = Story.query.all()
        return create_response({'stories': [s.to_dict() for s in stories]})

@app.route(STORIES, methods=['POST'])
def post_stories():
    data = request.get_json()
    new_story = Story(story_name = data['story_name'])
    db.session.add(new_story)
    db.session.flush()

    data['poi_ids'] = data['poi_ids'] if 'poi_ids' in data else []
    if(len(data['poi_ids']) != 0):
        ids = data['poi_ids']
        for i in ids:
            new_story_poi = StoryPOI(story_id = new_story.id, poi_id = i)
            db.session.add(new_story_poi)
    db.session.commit()
    story_dict = new_story.to_dict()
    story_dict['id'] = new_story.id
    return create_response({'story': story_dict})

#
# nums = [1,2,3]
#
# new_list = []
# for i in l:
#     new_list.append(i + 1)
#
# [i + 1 for i in nums if i % 2 == 1]



# @app.route(STORIES, methods=['PUT'])
# def put_stories():
#     data = request.get_json()
