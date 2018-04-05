from api import app, db
from api.models import Story, StoryPOI, POI
from api.utils import create_response, row_constructor
from flask import Blueprint, request

SEARCH_URL = "/search"

mod = Blueprint('search', __name__)

@app.route(SEARCH_URL, methods=['GET'])
def search_pois():
    data = request.args
    pois = []

    if data.get('name') is not None:
        # pois = POI.query.filter(POI.name.contains(data['name']))

    if pois.count() == 0:
        return create_response(status=404, message='No POIs found')
    pois_list = [poi_links_media_stories(i.to_dict()) for i in pois]
    return create_response({'pois': pois_list})
