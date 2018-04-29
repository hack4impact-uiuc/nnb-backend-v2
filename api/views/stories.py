from api import app, db
from api.models import Story, StoryPOI
from api.utils import create_response, row_constructor
from api.auth_tokens import token_required
from flask import Blueprint, request

mod = Blueprint('stories', __name__)

STORIES_URL = "/stories"
STORIES_ID_URL = "/stories/<int:story_id>"

@app.route(STORIES_URL, methods=['GET'])
def get_stories():
    data = request.args
    stories = []
    if data.get('poi_id') is not None:
        storyPOIs = StoryPOI.query.filter(StoryPOI.poi_id == data['poi_id'])
        for sp in storyPOIs:
            stories.append(Story.query.get(sp.story_id))
        return create_response({'stories': [s.to_dict() for s in stories]})
    stories = Story.query.all()
    return create_response({'stories': [s.to_dict() for s in stories]})

@app.route(STORIES_URL, methods=['POST'])
@token_required
def post_stories():
    data = request.get_json()
    if data.get('story_name') is not None:
        new_story = row_constructor(Story, data)
    else:
        return create_response(status=422, message='The story_name parameter was not provided or is invalid')
    db.session.add(new_story)
    db.session.flush()
    if data.get('poi_ids') is not None:
        new_story_pois = [row_constructor(StoryPOI, story_id=new_story.id, poi_id=poi_id) for poi_id in data['poi_ids']]
        db.session.add_all(new_story_pois)
    db.session.commit()
    story = Story.query.get(new_story.id)
    return create_response(data={'story': story.to_dict()}, status=201, message='Story created')

@app.route(STORIES_ID_URL, methods=['PUT'])
@token_required
def put_stories(story_id):
    data = request.get_json()
    fields = ['story_name', 'poi_ids']
    missing_params = [field for field in fields if data.get(field) is None]
    if len(missing_params) == 2:
        message = 'Must provide at least one of the following parameters: story_name or poi_ids'
        return create_response(data, 422, message)

    story = Story.query.get(story_id)
    if data.get('story_name') is not None:
        story.story_name = data['story_name']
        db.session.commit()

    if data.get('poi_ids') is not None:
        StoryPOI.query.filter(StoryPOI.story_id == story_id).delete()
        if(len(data['poi_ids']) > 0):
            new_story_pois = [row_constructor(StoryPOI, story_id=story_id, poi_id=poi_id) for poi_id in data['poi_ids']]
            db.session.add_all(new_story_pois)
            db.session.commit()

    story = Story.query.get(story_id)
    return create_response(data={'story': story.to_dict()}, message='Story updated')

@app.route(STORIES_ID_URL, methods=['DELETE'])
@token_required
def delete_stories(story_id):
    to_delete = Story.query.get(story_id)
    if to_delete is None:
        return create_response(status=404, message='Provided story_id does not exist')
    db.session.delete(to_delete)
    db.session.commit()
    return create_response(message='Story deleted')
