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
        pois = POI.query.filter(POI.name.like(data['name']))

    if pois.count() == 0:
        return create_response(status=404, message='No POIs found')
    return create_response({'pois_list': [p.to_dict() for p in pois]})
