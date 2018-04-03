from api import app, db
from api.models import Story, StoryPOI, POI
from api.utils import create_response, row_constructor
from flask import Blueprint, request

SEARCH_URL = "/stories"

mod = Blueprint('search', __name__)

@app.route(SEARCH_URL, methods=['GET'])
def get_pois():
    name = request.args.get('name')

    if name is not None:
        # do stuff

    if pois.count() == 0:
        return create_response(status=404, message='No POIs found')
    pois_list = [poi_links_media_stories(i.to_dict()) for i in pois]
    return create_response({'pois': pois_list})
