from api import app, db
from api.models import POI, Media, Link, Story, StoryPOI
from api.utils import create_response, InvalidUsage
from sqlalchemy.sql.expression import func
from flask import Blueprint, request, jsonify
import json
from datetime import date
from dateutil.parser import parse

mod = Blueprint('POIS', __name__)

def poi_links_media_stories(poi_dict):
    """
    Gets additional links, media, and stories for a POI
    """
    poi_links = Link.query.filter(Link.poi_id == poi_dict['_id'])
    poi_media = Media.query.filter(Media.poi_id == poi_dict['_id'])
    poi_stories = Story.query.join(StoryPOI, Story.id == StoryPOI.story_id).filter(StoryPOI.poi_id == poi_dict['_id'])
    poi_dict['links'] = [j.to_dict() for j in poi_links]
    poi_dict['media'] = [k.to_dict() for k in poi_media]
    poi_dict['stories'] = [l.to_dict() for l in poi_stories]
    return poi_dict

@app.route('/pois', methods=['GET'])
def pois_get_by_map_year_or_story():
    map_year, story_id = request.args.get('map_year'), request.args.get('story_id')
    if map_year is not None and story_id is None:
        # Find POIs by map_year
        pois = POI.query.filter(POI.map_year == int(map_year))
        if pois.count() == 0:
            return create_response(status=404, message='No POIs found')
    elif story_id is not None and map_year is None:
        # Find POIs by story_id
        pois = POI.query.join(StoryPOI, POI.id == StoryPOI.poi_id).filter(StoryPOI.story_id == int(story_id))
        if pois.count() == 0:
            return create_response(status=404, message='No POIs found')
    # Add associated links, media, and stories to each POI, then create a list of all POIs
    pois_list = [poi_links_media_stories(i.to_dict()) for i in pois]
    return create_response({'pois': pois_list})

@app.route('/pois/<poi_id>', methods=['GET'])
def pois_get_by_id(poi_id):
    poi_by_id = POI.query.get(int(poi_id))
    if poi_by_id is None:
        return create_response(status=404, message='No POI found')
    # Find associated links, media, and stories
    poi_result = poi_links_media_stories(poi_by_id.to_dict())
    return create_response({'poi': poi_result})

@app.route('/pois', methods=['POST'])
def pois_post():
    data = request.get_json()
    # Check that all required parameters exist
    if not all(i is not None for i in [data['name'], data['description'], data['map_year'], data['x_coord'], data['y_coord']]):
        return create_response(status=422, messsage='POI not created; missing one or more required input parameters')
    for j in data['links']:
        if j['link_url'] is None:  # Check for link url in each link
            return create_response(status=422, message='POI not created; missing link URL')
    for k in data['media']:
        if k['content_url'] is None:  # Check for content url in each medium
            return create_response(status=422, message='POI not created; missing media URL')
    for l in data['story_ids']:
        if Story.query.get(l) is None:  # Check if story exists for each story_id
            return create_response(status=422, message='POI not created; story_id does not exist')
    # Check if date exists; default to Jan 1 of map_year
    data['date'] = data['date'] if data['date'] is not None else date(map_year, 1, 1)
    # Add to POI table in db
    poi_add = POI(name=data['name'],
                  date=data['date'],
                  description=data['description'],
                  map_year=data['map_year'],
                  x_coord=data['x_coord'],
                  y_coord=data['y_coord'])
    db.session.add(poi_add)
    db.session.commit()
    # Add to Link, Media, and StoryPOI tables in db
    poi_id = db.session.query(func.max(POI.id)).scalar() # poi_id of the new POI
    link_add = [Link(link_url=j['link_url'],
                     display_name=j['display_name'],
                     poi_id=poi_id) for j in data['links']]
    media_add = [Media(content_url=k['content_url'],
                       caption=k['caption'],
                       poi_id=poi_id) for k in data['media']]
    story_add = [StoryPOI(story_id=l,
                          poi_id=poi_id) for l in data['story_ids']]
    db.session.add_all(link_add)
    db.session.add_all(media_add)
    db.session.add_all(story_add)
    db.session.commit()
    created_poi = POI.query.get(poi_id)  # Getting the newly created POI for create_response
    response_data = {'poi': poi_links_media_stories(created_poi.to_dict())}
    return create_response(data=response_data, status=201, message='POI created')

@app.route('/pois/<poi_id>', methods=['PUT'])
def pois_put(poi_id):
    data = request.get_json()
    return create_response(data)

@app.route('/pois/<poi_id>', methods=['DELETE'])
def pois_delete(poi_id):
    poi_to_delete = POI.query.get(poi_id)
    db.session.delete(poi_to_delete)
    db.session.commit()
    return create_response(message='POI deleted')