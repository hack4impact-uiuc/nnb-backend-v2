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

# json objects to be tested
map_add_json_1 = {
    "map_year" : 1669,
    "image_url": 'http://www.arizona-leisure.com/gfx/maps/valley-sun-map-760.gif'
 }

map_add_json_2 = {
    "map_year" : 1670,
    "image_url": 'http://www.fultonranchtownecenter.com/Post/sections/11/Images/FR_MasterPlan.jpg',
}

map_add_json_3 = {
    "map_year" : 3000,
    "image_url" : "https://pcavote.files.wordpress.com/2015/12/jonas-brothers-reunion.jpg"
}

map_add_json_bad_1 = {
    "image_url": 'http://www.fultonranchtownecenter.com/Post/sections/11/Images/FR_MasterPlan.jpg'
}

map_add_json_bad_2 = {
    "map_year": 2000
}

map_add_json_bad_3 = {

}

poi_add_json_1 = {
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

poi_add_json_2 = {
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

poi_add_json_3 = {
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

def find_map_occurence(map_obj):
    data = requests.get('http://127.0.0.1:5000/maps')
    map_year = map_obj['map_year']
    map_year_list = list(filter(lambda x: x['map_year'], data.json()['result']['maps']))
    while map_year in map_year_list:
        map_year = random.randInt(1800,2018)
    map_obj['map_year'] = map_year

# def find_non_existent_id():
#     _id = 13



class MapTests(unittest.TestCase):
 # this is a comprensive test suite for testing the map end points

    def test_map_post_get(self):
        # testing 1 post and 1 get
        find_map_occurence(map_add_json_1)
        post_data = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_1)
        get_data = requests.get('http://127.0.0.1:5000/maps')

        post_data_body = post_data.json()['result']['map']
        get_data_body = get_data.json()['result']['maps']
        self.assertEqual(post_data.json()['code'], 201)
        self.assertEqual(get_data.json()['code'], 200)

        map_id_list = [x['_id'] for x in get_data_body]
        map_posted = post_data_body['_id'] in map_id_list
        self.assertEqual(True, map_posted)

        # is there a way to shorten this ?

        map_in_list = None
        for map_obj in get_data_body:
            if map_obj['_id'] == post_data_body['_id']:
                map_in_list = map_obj
                break

        self.assertEqual(post_data_body['map_year'], map_in_list['map_year'])
        self.assertEqual(post_data_body['image_url'], map_in_list['image_url'])

    def test_map_post_get_delete_bad(self):
        # test that the proper status_code is returned given bad requests
        before_get = requests.get('http://127.0.0.1:5000/maps')
        before_size = len(before_get.json()['result']['maps'])

        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_bad_1)
        self.assertEqual(response.json()['code'], 400)

        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_bad_2)
        self.assertEqual(response.json()['code'], 400)

        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_bad_3)
        self.assertEqual(response.json()['code'], 400)

        id = 1
        while id in list(filter(lambda x: x['_id'], before_get.json()['result']['maps'])):
            id+=1
        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(id))
        self.assertEqual(response.json()['status'], 404)

        after_get = requests.get('http://127.0.0.1:5000/maps')
        after_size = len(after_get.json()['result']['maps'])
        self.assertEqual(before_size,after_size)

        # This test suite is under the assumption that the post_poi/get_poi
        # is fully functional.

    def test_map_delete(self):

        # tests the delete functionality and checks that the pois are deleted as
        # well
        find_map_occurence(map_add_json_3)
        poi_add_json_1['map_year'] = map_add_json_3['map_year']
        poi_add_json_2['map_year'] = map_add_json_3['map_year']
        poi_add_json_3['map_year'] = map_add_json_3['map_year']

        requests.post('http://127.0.0.1:5000/pois', json = poi_add_json_1)
        requests.post('http://127.0.0.1:5000/pois', json = poi_add_json_2)
        requests.post('http://127.0.0.1:5000/pois', json = poi_add_json_3)

        post_data = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_3)
        post_data_body = post_data.json()['result']['map']
        id = post_data_body['_id']
        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(id))
        self.assertEqual(response.json()['status'], 200)

        data = requests.get('http://127.0.0.1:5000/maps')
        response_data = data.json()['result']['maps']
        map_deleted = id not in list(filter(lambda x: x['_id'], get_data_body))
        self.assertEqual(True,map_deleted)

        pois_response = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(post_data_body['map_year']))
        self.assertEqual(pois_response.json()['code'], 404)
