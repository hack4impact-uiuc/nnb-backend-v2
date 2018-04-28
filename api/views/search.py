from api import app, db
from api.models import POI
from api.views.pois import poi_links_media_stories
from api.utils import create_response
from flask import Blueprint, request
from sqlalchemy import func

SEARCH_POIS_URL = "/search/pois"

mod = Blueprint('search', __name__)

@app.route(SEARCH_POIS_URL, methods=['GET'])
def search_pois():
    data = request.args
    pois_by_name = []
    pois_by_description = []
    pois = []

    if (data.get('q') and data.get('name') and data.get('description')) is None:
        return create_response(status=404, message='Must include query, name, and description parameters.')

    if data.get('name') == "true":
        pois_by_name = POI.query.filter(func.lower(POI.name).contains(data['q'].lower()))
    if data.get('description') == "true":
        pois_by_description = POI.query.filter(func.lower(POI.description).contains(data['q'].lower()))

    pois_by_name_list = [poi_links_media_stories(p.to_dict()) for p in pois_by_name]
    pois_by_description_list = [poi_links_media_stories(p.to_dict()) for p in pois_by_description]
    for p in pois_by_name_list:
        if p not in pois_by_description_list:
            pois.append(p)
    pois += pois_by_description_list
    return create_response({'pois': pois})
