from api import app, db
from api.models import POI, Media, Link, Story, StoryPOI
from api.utils import create_response, row_constructor
from flask import Blueprint, request, jsonify
import json
from datetime import date
from dateutil.parser import parse

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

@app.route('/pois', methods=['GET'])
def pois_get_by_map_year_or_story():
    map_year = request.args.get('map_year')
    story_id = request.args.get('story_id')

    # Find POIs by map_year
    if map_year is not None and story_id is None:
        pois = POI.query.filter(POI.map_year == int(map_year))

    # Find POIs by story_id
    elif story_id is not None and map_year is None:
        pois = POI.query.join(StoryPOI, POI.id == StoryPOI.poi_id) \
                        .filter(StoryPOI.story_id == int(story_id))

    if pois.count() == 0:
        return create_response(status=404, message='No POIs found')
    pois_list = [poi_links_media_stories(i.to_dict()) for i in pois]
    return create_response({'pois': pois_list})

@app.route('/pois/<poi_id>', methods=['GET'])
def pois_get_by_id(poi_id):
    poi_by_id = POI.query.get(int(poi_id))
    if poi_by_id is None:
        return create_response(status=404, message='No POI found')
    poi_result = poi_links_media_stories(poi_by_id.to_dict())
    return create_response({'poi': poi_result})

@app.route('/pois', methods=['POST'])
def pois_post():
    data = request.get_json()

    # Check that all required parameters exist
    if not all(i in data for i in ('name', 'description', 'map_year', 'x_coord', 'y_coord')):
        return create_response(status=422, message='POI not created; missing required input parameter(s)')
    for j in data['links']:
        if 'link_url' not in j:
            return create_response(status=422, message='POI not created; missing link URL')
    for k in data['media']:
        if 'content_url' not in k:
            return create_response(status=422, message='POI not created; missing media URL')

    # Check if story exists for each story_id
    for _id in data['story_ids']:
        if Story.query.get(_id) is None:
            return create_response(status=422, message='POI not created; story_id {} does not exist'.format(_id))

    # Check if date exists; default to Jan 1 of map_year
    data['date'] = parse(data['date']) if data['date'] is not None else date(map_year, 1, 1)

    # Add to POI table in db
    poi_add = row_constructor(POI, data)
    db.session.add(poi_add)
    db.session.flush()

    # Add to Link, Media, and StoryPOI tables in db
    poi_id = poi_add.id
    link_add = [row_constructor(Link, j, poi_id=poi_id) for j in data['links']]
    media_add = [row_constructor(Media, k, poi_id=poi_id) for k in data['media']]
    story_add = [row_constructor(StoryPOI, story_id=_id, poi_id=poi_id) for _id in data['story_ids']]
    db.session.add_all(link_add)
    db.session.add_all(media_add)
    db.session.add_all(story_add)
    db.session.commit()

    # Get the newly created POI for create_response
    created_poi = POI.query.get(poi_id)
    response_data = {'poi': poi_links_media_stories(created_poi.to_dict())}
    return create_response(response_data, 201, 'POI created')

@app.route('/pois/<poi_id>', methods=['PUT'])
def pois_put(poi_id):
    poi_by_id = POI.query.get(int(poi_id))
    if poi_by_id is None:
        return create_response(status=404, message='No POI found')
    data = request.get_json()
    if 'name' is in data:
        poi_by_id.name = data['name']
    if 'date' is in data:
        poi_by_id.date = parse(data['date'])
    if 'description' is in data:
        poi_by_id.description = data['description']
    if 'story_ids' is in data:
        for i in data['story_ids']:
            if Story.query.get(i) is None:
                return create_response(status=422, message='POI not created; story_id {} does not exist'.format(i))
        for j in StoryPOI.query.filter(StoryPOI.poi_id == poi_id):
            db.session.delete(j)
        story_add = [row_constructor(StoryPOI, story_id=_id, poi_id=poi_id) for _id in data['story_id']]
    if 'media' is in data:
        for i in Media.query.filter(Media.poi_id == poi_id):
            db.session.delete(i)
        media_add = [row_constructor(Media, k, poi_id=poi_id) for k in data['media']]
    if 'links' is in data:
        for i in Link.query.filter(Link.poi_id == poi_id):
            db.session.delete(i)
        link_add = [row_constructor(Link, j, poi_id=poi_id) for j in data['links']]
    db.session.add_all(story_add)
    db.session.add_all(media_add)
    db.session.add_all(link_add)
    db.session.commit()
    #Can I just use pois_by_id?
    edited_poi = POI.query.get(int(poi_id))
    response_data = {'poi': poi_links_media_stories(edited_poi.to_dict())}
    return create_response(response_data, 201, 'POI edited')

@app.route('/pois/<poi_id>', methods=['DELETE'])
def pois_delete(poi_id):
    poi_to_delete = POI.query.get(poi_id)
    if poi_to_delete is None:
        return create_response(status=404, message='No POI found')
    db.session.delete(poi_to_delete)
    db.session.commit()
    return create_response(message='POI deleted')
