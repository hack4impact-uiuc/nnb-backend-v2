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
def id_to_url(map_id):
    return MAPS_URL + '/{}'.format(map_id)

# json objects to be tested
good_map = {
    'map_year' : 1669,
    'image_url': 'http://www.arizona-leisure.com/gfx/maps/valley-sun-map-760.gif'
}

bad_maps = []
bad_maps.append(
    {
        'image_url': 'http://www.fultonranchtownecenter.com/Post/sections/11/Images/FR_MasterPlan.jpg'
    }
)
bad_maps.append(
    {
        'map_year': 2000
    }
)
bad_maps.append({})

pois = []
pois.append(
    {
        'name' : 'The battle of the Bulge',
        'date' : '5/20',
        'description' : 'people died',
        'map_year' : 3000,
        'x_coord' : '5',
        'y_coord' : '7',
        'links': [],
        'media': [],
        'story_ids': []
    }
)
pois.append(
    {
        'name' : 'The Great Herbal Fire',
        'date' : '4/20',
        'description' : 'An uplifting experience for many people',
        'map_year' : 3000,
        'x_coord' : '7',
        'y_coord' : '5',
        'links': [],
        'media': [],
        'story_ids': []
    }
)
pois.append(
    {
        'name' : 'Nithin Becomes a Man',
        'date' : '2/4',
        'description' : 'Nothing really',
        'map_year' : 3000,
        'x_coord' : '8',
        'y_coord' : '9',
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


# this is a comprensive test suite for testing the map end points
class MapTests(unittest.TestCase):
    def test_map(self):
        self.map_id = -1
        self.test_map_post()
        self.test_map_get()
        self.test_map_delete()
    
    def test_map_post(self):
        # test good map
        find_unique_year(good_map)
        response = requests.post(MAPS_URL, json=good_map)
        response_json = response.json()
        self.assertEqual(response_json['code'], 201)
        response_map = response_json['result']['map']
        self.assertEqual(response_map['map_year'], good_map['map_year'])
        self.assertEqual(response_map['image_url'], good_map['image_url'])
        self.map_id = response_map['_id']
        # test bad maps
        for bad_map in bad_maps:
            result = requests.post(MAPS_URL, json=bad_map)
            result_json = result.json()
            self.assertEqual(result_json['code'], 400)
            result_data = result_json['result']
            self.assertEqual(bad_map, result_data)

    # checks if a map is in the get response maps list. helper for get
    def id_in_maps(self, map_id):
        response = requests.get(MAPS_URL)
        response_json = response.json()
        self.assertEqual(response_json['code'], 200)
        response_maps = response_json['result']['maps']
        for map in response_maps:
            if map['_id'] == self.map_id:
                self.assertEqual(map['map_year'], good_map['map_year'])
                self.assertEqual(map['image_url'], good_map['image_url'])
                return True
        return False

    # assumes post worked
    def test_map_get(self):
        # testing good map is in list
        self.assertTrue(self.id_in_maps(self.map_id))

    # assumes post worked
    def test_map_delete(self):
        # test delete on nonexistent map
        bad_response = requests.delete(id_to_url(-1))
        self.assertEqual(bad_response.json()['status'], 404)
        # test delete on good_map
        response = requests.delete(id_to_url(self.map_id))
        self.assertEqual(response.json()['code'], 200)
        # check that good_map no longer in list
        self.assertFalse(self.id_in_maps(self.map_id))