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
    pois1 = []
    pois2 = []

    if data.get('q') is not None:
        if data.get('name') is not None:
            if data.get('name') == "True":
                pois1 = POI.query.filter(POI.name.contains(data['q']))
        if data.get('description') is not None:
            if data.get('description') == "True":
                pois2 = POI.query.filter(POI.description.contains(data['q']))

    if pois1.count() == 0 and pois2.count() == 0:
        return create_response(status=404, message='No POIs found')
    list1 = [p.to_dict() for p in pois1]
    list2 = [p.to_dict() for p in pois2]
    pois = list1 + list2
    return create_response({'pois_list': pois})
