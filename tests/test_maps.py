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
    "map_year" : 1669,
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
    "map_year" : 1670,
    "x_coord" : "8",
    "y_coord" : "9",
    'links': [],
    'media': [],
    'story_ids': []
}



def clear_database():
    Map.query.delete()
    db.session.commit()

class MapTests(unittest.TestCase):
 # this is a comprensive test suite for testing the map end points

    def test_map_post_get(self):
        clear_database()
        # testing 1 post and 1 get
        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_1)
        data = requests.get('http://127.0.0.1:5000/maps')

        response_data = data.json()['result']['maps']
        self.assertEqual(response.json()['code'], 201)
        self.assertEqual(data.json()['code'], 200)
        self.assertEqual(response_data[0]['map_year'], 1669)
        self.assertEqual(response_data[0]['image_url'], 'http://www.arizona-leisure.com/gfx/maps/valley-sun-map-760.gif')
        # testing an additional post and see if all maps in db are retrieved
        response = requests.post('http://127.0.0.1:5000/maps', json = map_add_json_2)
        data = requests.get('http://127.0.0.1:5000/maps')

        response_data = data.json()['result']['maps']
        self.assertEqual(response.json()['code'], 201)
        self.assertEqual(data.json()['code'], 200)
        self.assertEqual(response_data[1]['map_year'], 1670)
        self.assertEqual(response_data[1]['image_url'], 'http://www.fultonranchtownecenter.com/Post/sections/11/Images/FR_MasterPlan.jpg')
        # testing one last map
        response = requests.post('http://127.0.0.1:5000/maps', json = map_add_json_3)
        data = requests.get('http://127.0.0.1:5000/maps')


        response_data = data.json()['result']['maps']
        self.assertEqual(response.json()['code'], 201)
        self.assertEqual(data.json()['code'], 200)
        self.assertEqual(len(response_data),3)
        self.assertEqual(response_data[2]['map_year'], 3000)
        self.assertEqual(response_data[2]['image_url'], "https://pcavote.files.wordpress.com/2015/12/jonas-brothers-reunion.jpg")
        # test that the proper status_code is returned given bad requests
        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_bad_1)
        self.assertEqual(response.json()['code'], 400)

        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_bad_2)
        self.assertEqual(response.json()['code'], 400)

        response = requests.post('http://127.0.0.1:5000/maps', json= map_add_json_bad_3)
        self.assertEqual(response.json()['code'], 400)

        response = requests.delete('http://127.0.0.1:5000/maps/4')
        self.assertEqual(response.json()['code'], 404)

        data = requests.get('http://127.0.0.1:5000/maps')
        response_data_before = data.json()['result']['maps']
        self.assertEqual(len(response_data),3)
        # This test suite is under the assumption that the post_poi/get_poi
        # is fully functional.
        requests.post('http://127.0.0.1:5000/pois', json = poi_add_json_1)
        requests.post('http://127.0.0.1:5000/pois', json = poi_add_json_2)
        requests.post('http://127.0.0.1:5000/pois', json = poi_add_json_3)
        # tests the delete functionality and checks that the pois are deleted as
        # well
        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(response_data_before[0]['_id']))
        self.assertEqual(response.json()['code'], 200)
        data = requests.get('http://127.0.0.1:5000/maps')
        response_data = data.json()['result']['maps']
        self.assertEqual(len(response_data),2)

        map_year = response_data_before[0]['map_year']
        pois_response = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        self.assertEqual(pois_response.json()['code'], 404)

        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(response_data[0]['_id']))
        self.assertEqual(response.json()['code'], 200)
        data = requests.get('http://127.0.0.1:5000/maps')
        response_data = data.json()['result']['maps']
        self.assertEqual(len(response_data),1)

        map_year = response_data_before[0]['map_year']
        pois_response = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        self.assertEqual(pois_response.json()['code'], 404)

        response = requests.delete('http://127.0.0.1:5000/maps/{}'.format(response_data[0]['_id']))
        self.assertEqual(response.json()['code'], 200)
        data = requests.get('http://127.0.0.1:5000/maps')
        response_data = data.json()['result']['maps']
        self.assertEqual(len(response_data),0)

        map_year = response_data_before[0]['map_year']
        pois_response = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        self.assertEqual(pois_response.json()['code'], 404)
