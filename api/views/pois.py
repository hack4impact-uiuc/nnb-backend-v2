from api import app
from flask import Blueprint, request, jsonify
from api.models import POI, Media, Link, Story, StoryPOI
import json
from api.utils import create_response, InvalidUsage

mod = Blueprint('POIS', __name__)

def poi_links_media_stories(poi_dict):
    """
    Gets additional links, media, and stories for a POI
    """
    poi_links = Link.query.filter(Link.poi_id == poi_dict['_id'])
    poi_media = Media.query.filter(Media.poi_id == poi_dict['_id'])
    poi_stories = Story.query.join(StoryPOI, Story.id == StoryPOI.story_id).filter(StoryPOI.poi_id == poi_dict['_id'])
    poi_dict['links'] = [j.to_dict() for j in poi_links]
    poi_dict['media'] = [j.to_dict() for j in poi_media]
    poi_dict['stories'] = [j.to_dict() for j in poi_stories]
    return poi_dict

@app.route('/pois', methods=['GET'])
def pois_get_by_map_year_or_story():
    map_year, story_id = request.args.get('map_year'), request.args.get('story_id')
    if map_year is not None and story_id is None:
        pois = POI.query.filter(POI.map_year == int(map_year))
        if pois.count() == 0:
            return create_response(status=404, message='No POIs found')
    elif story_id is not None and map_year is None:
        pois = POI.query.join(StoryPOI, POI.id == StoryPOI.poi_id).filter(StoryPOI.story_id == int(story_id))
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
    return create_response(data)

@app.route('/pois/<poi_id>', methods=['PUT'])
def pois_put(poi_id):
    data = request.get_json()
    return create_response(data)

@app.route('/pois/<poi_id>', methods=['DELETE'])
def pois_delete(poi_id):
    return create_response(data)