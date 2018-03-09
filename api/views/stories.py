from api import app, db
from api.models import Story, StoryPOI
from api.utils import create_response, row_constructor
from flask import Blueprint, request

mod = Blueprint('stories', __name__)

STORIES_URL = "/stories"
STORIES_ID_URL = "/stories/<int:story_id>"

@app.route(STORIES_URL, methods=['GET'])
def get_stories():
    data = request.get_json()
    if 'poi_id' in data:
        stories = StoryPOI.query.filter(StoryPOI.poi_id == data['poi_id'])
        if stories.count() == 0:
            return create_response(status=404, message='No stories found for specified POI')
        else:
            return create_response({'stories': [s.to_dict() for s in stories]})
    else:
        stories = Story.query.all()
        return create_response({'stories': [s.to_dict() for s in stories]})

@app.route(STORIES_URL, methods=['POST'])
def post_stories():
    data = request.get_json()
    if 'story_name' in data:
        new_story = row_constructor(Story, data)
    else:
        return create_response(status=422, message='No story_name parameter was provided')
    db.session.add(new_story)
    db.session.flush()

    if 'poi_ids' in data:
        new_story_pois = [row_constructor(StoryPOI, story_id=new_story.id, poi_id=poi_id) for poi_id in data['poi_ids']]
        db.session.add_all(new_story_pois)
    db.session.commit()
    story = Story.query.get(new_story.id)
    return create_response(data = {'story': story.to_dict()}, message = 'Story created')

@app.route(STORIES_ID_URL, methods=['PUT'])
def put_stories(story_id):
    data = request.get_json()
    story = Story.query.get(story_id)
    if 'story_name' in data:
        story.story_name = data['story_name']
    if 'poi_ids' in data:
        StoryPOI.query.filter(StoryPOI.story_id == story_id).delete()
        if(len(data['poi_ids']) > 0):
            new_story_pois = [row_constructor(StoryPOI, story_id = story_id, poi_id = poi_id) for poi_id in data['poi_ids']]
            db.session.add_all(new_story_pois)
            db.session.commit()
    story = Story.query.get(story_id)
    return create_response(data = {'story': story.to_dict()}, message = 'Story updated')

@app.route(STORIES_ID_URL, methods = ['DELETE'])
def delete_stories(story_id):
    to_delete = Story.query.get(story_id)
    if to_delete.count() == 0:
        return create_response(status=404, message='Provided story_id does not exist')
    db.session.delete(to_delete)
    StoryPOI.query.filter(StoryPOI.story_id == story_id).delete()
    db.session.commit()
    return create_response(message = 'Story deleted')
