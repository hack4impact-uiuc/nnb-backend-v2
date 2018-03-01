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
    return create_response(data = {'story': story_dict}, message = 'Story created')

 @app.route(STORIES_PARAM, methods=['PUT'])
def put_stories(story_id):
    data = request.get_json()
    new_story_name = data['story_name'] if 'story_name' in data else ''
    new_poi_ids = data['poi_ids'] if 'poi_ids' in data else []
    story = Story.query.get(story_id)
    if(len(new_story_name) != 0):
    	story.story_name = new_storm_name
    StoryPOI.query.filter(StoryPOI.story_id == story_id).delete()
    if(len(new_poi_ids) != 0):
    	for i in new_poi_ids:
    		new_story_poi = StoryPOI(story_id = story_id, poi_id = i)
    		db.session.add(new_story_poi)
    db.session.commit()
    return create_response(data = {'story': story.to_dict()}, message = 'Story updated')


@app.route(STORIES_PARAM, methods = ['DELETE'])
def delete_stories(story_id):
	Story.query.filter(Story.story_id == story_id).delete()
	StoryPOI.query.filter(StoryPOI.story_id == story_id).delete()
	db.session.commit()
	return create_response(message = 'Story deleted')
