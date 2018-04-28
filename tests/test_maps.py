import os
import unittest
from flask import jsonify
from api import db
from flask import Flask, request
from api.models import Map
from api.models import POI
import requests
from flask import jsonify
import json

MAPS_URL = 'http://127.0.0.1:5000/maps'
# json objects to be tested
good_map = {
    "map_year" : 1669,
    "image_url": 'http://www.arizona-leisure.com/gfx/maps/valley-sun-map-760.gif'
}

bad_maps = []
bad_maps.append(
    {
        "image_url": 'http://www.fultonranchtownecenter.com/Post/sections/11/Images/FR_MasterPlan.jpg'
    }
)
bad_maps.append(
    {
        "map_year": 2000
    }
)
bad_maps.append({})

pois = []
pois.append(
    {
        "name" : "The battle of the Bulge",
        "date" : "5/20",
        "description" : "people died",
        "map_year" : 3000,
        "x_coord" : "5",
        "y_coord" : "7",
        'links': [],
        'media': [],
        'story_ids': []
    }
)
pois.append(
    {
        "name" : "The Great Herbal Fire",
        "date" : "4/20",
        "description" : "An uplifting experience for many people",
        "map_year" : 3000,
        "x_coord" : "7",
        "y_coord" : "5",
        'links': [],
        'media': [],
        'story_ids': []
    }
)
pois.append(
    {
        "name" : "Nithin Becomes a Man",
        "date" : "2/4",
        "description" : "Nothing really",
        "map_year" : 3000,
        "x_coord" : "8",
        "y_coord" : "9",
        'links': [],
        'media': [],
        'story_ids': []
    }
)

# assigns map_obj a unique year not in the map list
def find_unique_year(map_obj):
    data = requests.get(MAPS_URL)
    map_year = map_obj['map_year']
    map_year_list = [x['map_year'] for x in data.json()['result']['maps']]
    while map_year in map_year_list:
        map_year +=1
    map_obj['map_year'] = map_year


class MapTests(unittest.TestCase):
    # this is a comprensive test suite for testing the map end points
    def test_map_post(self):
        # test good map
        find_unique_year(good_map)
        response = requests.post(MAPS_URL, json=good_map)
        response_json = response.json()
        self.assertEqual(response_json['code'], 201)
        response_map = response_json['result']['map']
        self.assertEqual(response_map['map_year'], good_map['map_year'])
        self.assertEqual(response_map['image_url'], good_map['image_url'])
        # test bad maps
        for bad_map in bad_maps:
            result = requests.post(MAPS_URL, json=bad_map)
            result_json = result.json()
            self.assertEqual(result_json['code'], 400)
            result_data = result_json['result']
            self.assertEqual(bad_map, result_data)

    # TODO
    def test_map_get(self):
        # testing 1 post and 1 get
        get_data = requests.get(MAPS_URL)
        get_data_json = get_data.json()
        get_data_body = get_data_json['result']['maps']
        self.assertEqual(get_data_json['code'], 200)

    # TODO
    def test_map_delete_bad(self):
        # test that the proper status_code is returned given bad requests
        before_get = requests.get(MAPS_URL)
        before_size = len(before_get.json()['result']['maps'])

        for map_bad_json in bad_maps:
            response = requests.post(MAPS_URL, json= map_bad_json)
            self.assertEqual(response.json()['code'], 400)

        id = 1
        while id in [x['_id'] for x in before_get.json()['result']['maps']]:
            id+=1
        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(id))
        self.assertEqual(response.json()['status'], 404)

        after_get = requests.get(MAPS_URL)
        after_size = len(after_get.json()['result']['maps'])
        self.assertEqual(before_size,after_size)

        # This test suite is under the assumption that the post_poi/get_poi
        # is fully functional.

    # TODO
    def test_map_delete_good(self):
        # tests the delete functionality and checks that the pois are deleted as
        # well
        find_unique_year(good_map)
        for poi_json in pois:
            poi_json['map_year'] = good_map['map_year']
            requests.post('http://127.0.0.1:5000/pois', json=poi_json)

        post_data = requests.post(MAPS_URL, json=good_map)
        post_data_body = post_data.json()['result']['map']
        id = post_data_body['_id']
        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(id))
        self.assertEqual(response.json()['status'], 200)

        get_data = requests.get(MAPS_URL)
        get_data_body = get_data.json()['result']['maps']
        map_deleted = id not in [x['_id'] for x in get_data_body]
        self.assertTrue(map_deleted)

        pois_response = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(post_data_body['map_year']))
        self.assertEqual(pois_response.json()['code'], 404)