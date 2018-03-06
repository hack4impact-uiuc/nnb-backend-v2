from api import app, db
from api.models import POI, Media, Link, Story, StoryPOI
from api.utils import create_response, row_constructor
from flask import Blueprint, request, jsonify
import json
from datetime import date
from dateutil.parser import parse

POIS_URL = '/pois'
POIS_ID_URL = '/pois/<int:poi_id>'

mod = Blueprint('pois', __name__)

def poi_links_media_stories(poi_dict):
    """
    Gets additional links, media, and stories for a POI
    """
    poi_links = Link.query.filter(Link.poi_id == poi_dict['_id'])
    poi_media = Media.query.filter(Media.poi_id == poi_dict['_id'])
    poi_stories = Story.query.join(StoryPOI, Story.id == StoryPOI.story_id) \
                             .filter(StoryPOI.poi_id == poi_dict['_id'])
    poi_dict['links'] = [j.to_dict() for j in poi_links]
    poi_dict['media'] = [k.to_dict() for k in poi_media]
    poi_dict['stories'] = [l.to_dict() for l in poi_stories]
    return poi_dict

@app.route(POIS_URL, methods=['GET'])
def get_pois():
    map_year = request.args.get('map_year')
    story_id = request.args.get('story_id')

    if bool(map_year) == bool(story_id):
        return create_response(
            status=400,
            message='Provided both or neither of map_year and story_id'
        )

    if map_year is not None and story_id is None:
        pois = POI.query.filter(POI.map_year == int(map_year))
    elif story_id is not None and map_year is None:
        pois = POI.query.join(StoryPOI, POI.id == StoryPOI.poi_id) \
                        .filter(StoryPOI.story_id == int(story_id))

    if pois.count() == 0:
        return create_response(status=404, message='No POIs found')
    pois_list = [poi_links_media_stories(i.to_dict()) for i in pois]
    return create_response({'pois': pois_list})

@app.route(POIS_ID_URL, methods=['GET'])
def get_poi_by_id(poi_id):
    poi = POI.query.get(int(poi_id))
    if poi is None:
        return create_response(status=404, message='POI not found')
    poi_result = poi_links_media_stories(poi.to_dict())
    return create_response({'poi': poi_result})

@app.route(POIS_URL, methods=['POST'])
def create_poi():
    data = request.get_json()

    data['links'] = data['links'] if 'links' in data else []
    data['media'] = data['media'] if 'media' in data else []
    data['story_ids'] = data['story_ids'] if 'story_ids' in data else []
    data['date'] = parse(data['date']) if 'date' in data else date(data['map_year'], 1, 1)

    # Check that all required parameters exist
    if not all(i in data for i in ('name', 'description', 'map_year', 'x_coord', 'y_coord')):
        return create_response(
            status=422,
            message='POI not created; missing required input parameter(s)'
        )
    for link in data['links']:
        if 'link_url' not in link:
            return create_response(
                status=422,
                message='POI not created; missing link URL'
            )
    for media in data['media']:
        if 'content_url' not in media:
            return create_response(
                status=422,
                message='POI not created; missing media URL'
            )

    for story_id in data['story_ids']:
        if Story.query.get(story_id) is None:
            return create_response(
                status=422,
                message='POI not created; story_id {} does not exist'.format(story_id)
            )

    poi_add = row_constructor(POI, data)
    db.session.add(poi_add)
    db.session.flush()
    poi_id = poi_add.id
    link_add = [row_constructor(Link, j, poi_id=poi_id) for j in data['links']]
    media_add = [row_constructor(Media, k, poi_id=poi_id) for k in data['media']]
    story_add = [row_constructor(StoryPOI, story_id=l, poi_id=poi_id) for l in data['story_ids']]
    db.session.add_all(link_add)
    db.session.add_all(media_add)
    db.session.add_all(story_add)
    db.session.commit()

    created_poi = POI.query.get(poi_id)
    response_data = {'poi': poi_links_media_stories(created_poi.to_dict())}
    return create_response(response_data, 201, 'POI created')

@app.route(POIS_ID_URL, methods=['PUT'])
def update_poi(poi_id):
    poi = POI.query.get(int(poi_id))
    if poi is None:
        return create_response(status=404, message='POI not found')
    data = request.get_json()

    # Edit poi columns
    if 'name' in data:
        poi.name = data['name']
    if 'date' in data:
        poi.date = parse(data['date'])
    if 'description' in data:
        poi.description = data['description']
    
    # Replace all links, media, and story_id if they were given
    if 'links' in data:
        for link in Link.query.filter(Link.poi_id == poi_id):
            db.session.delete(link)
        link_add = [row_constructor(Link, i, poi_id=poi_id) for i in data['links']]
        db.session.add_all(link_add)
    if 'media' in data:
        for media in Media.query.filter(Media.poi_id == poi_id):
            db.session.delete(media)
        media_add = [row_constructor(Media, i, poi_id=poi_id) for i in data['media']]
        db.session.add_all(media_add)
    if 'story_ids' in data:
        for story_id in data['story_ids']:
            if Story.query.get(story_id) is None:
                return create_response(
                    status=422,
                    message='POI not created; story_id {} does not exist'.format(i)
                )
        for story_id in StoryPOI.query.filter(StoryPOI.poi_id == poi_id):
            db.session.delete(story_id)
        story_add = [row_constructor(StoryPOI, story_id=i, poi_id=poi_id) for i in data['story_ids']]
        db.session.add_all(story_add)
    db.session.commit()

    edited_poi = POI.query.get(int(poi_id))
    response_data = {'poi': poi_links_media_stories(edited_poi.to_dict())}
    return create_response(response_data, 201, 'POI edited')

@app.route(POIS_ID_URL, methods=['DELETE'])
def delete_poi(poi_id):
    poi = POI.query.get(poi_id)
    if poi is None:
        return create_response(status=404, message='POI not found')
    db.session.delete(poi)
    db.session.commit()
    return create_response(message='POI deleted')
