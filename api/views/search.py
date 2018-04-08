from api import app, db
from api.models import POI
from api.utils import create_response
from flask import Blueprint, request

SEARCH_POIS_URL = "/search/pois"

mod = Blueprint('search', __name__)

@app.route(SEARCH_POIS_URL, methods=['GET'])
def search_pois():
    data = request.args
    pois_by_name = []
    pois_by_description = []

    if data.get('q') is not None:
        if data.get('name') is not None:
            if data.get('name') == "true":
                pois_by_name = POI.query.filter(POI.name.contains(data['q']))
        else:
            return create_response(status=404, message='Missing name parameter (true/false)')
        if data.get('description') is not None:
            if data.get('description') == "true":
                pois_by_description = POI.query.filter(POI.description.contains(data['q']))
        else:
            return create_response(status=404, message='Missing description parameter (true/false)')
    else:
        return create_response(status=404, message='Missing query parameter')

    pois_by_name_list = [p.to_dict() for p in pois_by_name]
    pois_by_description_list = [p.to_dict() for p in pois_by_description]
    pois = pois_by_name_list + pois_by_description_list
    return create_response({'pois': pois})
