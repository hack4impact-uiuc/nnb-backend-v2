import os
import unittest
from flask import jsonify
from api import app, db
from flask import Flask, request
from api.models import POI, Media, Link, Story, StoryPOI
import requests
from flask import jsonify
import json
from datetime import date

#Complete params

poi_create_complete = {
    'name': 'Morrow Plots',
    'date': '2018-03-05',
    'description': 'Just corn here',
    'map_year': 1856,
    'x_coord': 76,
    'y_coord': 42,
    'links': [
        {
            'link_url': 'http://fbnew.com',
            'display_name': 'FacebookNew'
        }
    ],
    'media': [
        {
            'content_url': 'http://images.com/alpaca.jpg',
            'caption': 'The new alpaca in its natural habitat'
        }
    ],
    'story_ids': [1, 2]
}

poi_update_complete = {
    'name': 'Morrow Plots',
    'date': '2018-03-05',
    'description': 'Just corn here',
    'links': [
        {
            'link_url': 'http://fbnew.com',
            'display_name': 'FacebookNew'
        }
    ],
    'media': [
        {
            'content_url': 'http://images.com/alpaca.jpg',
            'caption': 'The new alpaca in its natural habitat'
        }
    ],
    'story_ids': [1, 2]
}

#Permissible (only required attributes, optional ones not included)

poi_create_permissible = {
    #This one needs EITHER map_year OR story_ids
    'name': 'Morrow Plots',
    'date': '1856-01-01',
    'description': 'Just corn here',
    'map_year': 1856,
    'x_coord': 76,
    'y_coord': 42,
    'links': [],
    'media': [],
    'story_ids': []
}

poi_edit_permissible = {
    'name': 'Morrow Plots',
    #Technically date is not required, but frontend will automatically send in date as 1/1/mapyear
    #Otherwise there would be an error when running this test
    'date': '1856-01-01',
    'description': 'Just corn here',
    'links': [],
    'media': [],
    'story_ids': []
}

#Invalid

poi_create_invalid = {
    #Does not have name, description, map_year, x_coord, y_coord
    'name': '',
    'date': '01-01-00',
    'description': '',
    # 'map_year': ,
    # 'x_coord': ,
    'y_coord': 42,
    'links': [],
    'media': [],
    'story_ids': []
}

map_year_invalid = 0
story_id_invalid = 0
poi_id_invalid = 0

os.environ['POI_ID'] = '1' #initialize POI_ID as environment variable

class POITests(unittest.TestCase):

    def test0_1_create_poi(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_create_complete)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['poi']['name'], poi_create_complete['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit['date'])
        self.assertEqual(response['result']['poi']['description'], poi_create_complete['description'])
        self.assertEqual(response['result']['poi']['map_year'], poi_create_complete['map_year'])
        self.assertEqual(response['result']['poi']['x_coord'], poi_create_complete['x_coord'])
        self.assertEqual(response['result']['poi']['y_coord'], poi_create_complete['y_coord'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_create_complete['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_create_complete['links'][i]['display_name'])
        for j in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][j]['content_url'], poi_create_complete['media'][j]['content_url'])
            self.assertEqual(response['result']['poi']['media'][j]['caption'], poi_create_complete['media'][j]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_create_complete['story_ids']))
        os.environ['POI_ID'] = str(response['result']['poi']['_id'])

    def test0_2_get_poi_by_id(self, poi_id=0):
        if poi_id == 0:
            poi_id = int(os.environ.get('POI_ID'))
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['result']['poi']['_id'], poi_id)

        self.assertEqual(response['result']['poi']['name'], poi_create_complete['name'])
        # self.assertEqual(response['result']['poi']['date']
        self.assertEqual(response['result']['poi']['description'], poi_create_complete['description'])
        self.assertEqual(response['result']['poi']['map_year'], poi_create_complete['map_year'])
        self.assertEqual(response['result']['poi']['x_coord'], poi_create_complete['x_coord'])
        self.assertEqual(response['result']['poi']['y_coord'], poi_create_complete['y_coord'])

        #Account for time zones (see above commented out line)
        #Future Testing needed for links, media, stories (would require several loops based on json response)

    def test0_3_get_pois_by_map_year(self):
        map_year = poi_create_complete['map_year']

        #get request by map_year

        r1 = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        response1 = r1.json()

        self.assertEqual(response1['code'], 200)

        for i in response1['result']['pois']:
            self.test0_2_get_poi_by_id(poi_id = i['_id'])
            self.assertEqual(i['map_year'], map_year)

    def test0_3_get_pois_by_story_id(self):
        story_ids = poi_create_complete['story_ids']

        #get request by story_id

        for curr_story_id in story_ids:
            r2 = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(curr_story_id))
            response2 = r2.json()
            self.assertEqual(response2['code'], 200)
            #created_object_included is used to determine if the POI we previously created is included
            #in the list of POIs returned after we get request based on story_ids
            created_object_included = False
            for curr_poi in response2['result']['pois']:
                if curr_poi['name'] == poi_create_complete['name']:
                    created_object_included = True
            self.assertTrue(created_object_included)

    def test0_4_update_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_update_complete)
        response = r.json()
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['result']['poi']['name'], poi_update_complete['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_update_complete['date'])
        self.assertEqual(response['result']['poi']['description'], poi_update_complete['description'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_update_complete['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_update_complete['links'][i]['display_name'])
        for i in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][i]['content_url'], poi_update_complete['media'][i]['content_url'])
            self.assertEqual(response['result']['poi']['media'][i]['caption'], poi_update_complete['media'][i]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_update_complete['story_ids']))

    def test0_5_delete_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        self.assertEqual(response['code'], 200)

        r2 = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response2 = r2.json()
        self.assertEqual(response2['code'], 404)

    def test1_1_permissible(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_create_permissible)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['poi']['name'], poi_create_permissible['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit['date'])
        self.assertEqual(response['result']['poi']['description'], poi_create_permissible['description'])
        self.assertEqual(response['result']['poi']['map_year'], poi_create_permissible['map_year'])
        self.assertEqual(response['result']['poi']['x_coord'], poi_create_permissible['x_coord'])
        self.assertEqual(response['result']['poi']['y_coord'], poi_create_permissible['y_coord'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_create_permissible['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_create_permissible['links'][i]['display_name'])
        for j in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][j]['content_url'], poi_create_permissible['media'][j]['content_url'])
            self.assertEqual(response['result']['poi']['media'][j]['caption'], poi_create_permissible['media'][j]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_create_permissible['story_ids']))
        os.environ['POI_ID'] = str(response['result']['poi']['_id'])

    def test1_4_permissible(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_edit_permissible)
        response = r.json()
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['result']['poi']['name'], poi_edit_permissible['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_update_complete['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit_permissible['description'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit_permissible['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit_permissible['links'][i]['display_name'])
        for i in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][i]['content_url'], poi_edit_permissible['media'][i]['content_url'])
            self.assertEqual(response['result']['poi']['media'][i]['caption'], poi_edit_permissible['media'][i]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit_permissible['story_ids']))

    def test2_1_invalid(self):
        r = requests.post('http://127.0.0.1:5000/pois', json= poi_create_invalid)
        response = r.json()
        self.assertEqual(response['code'], 422)

    def test2_2_invalid(self, poi_id=0):
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id_invalid))
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test2_3_invalid(self):
        r1 = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year_invalid))
        r2 = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(story_id_invalid))
        response1 = r1.json()
        response2 = r2.json()
        #map_year_invalid
        self.assertEqual(response1['code'], 404)
        self.assertEqual(response2['code'], 404)

    def test2_5_invalid(self):
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id_invalid))
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test3_1_None(self):
        r = requests.post('http://127.0.0.1:5000/pois', json= None)
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test3_4_None(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json= None)
        response = r.json()
        self.assertEqual(response['code'], 404)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(POITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
