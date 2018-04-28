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

# Complete POI (all required and optional attributes)
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

# Valid Update. POI keys correspond to None values, but still valid because updates nothing
poi_update_none = {
    'name': None,
    'date': None,
    'description': None,
    'links': None,
    'media': None,
    'story_ids': None
}

# Invalid POI (missing required POIs)
poi_create_invalid = {
    'date': '01-01-00',
    'links': [],
    'media': [],
    'story_ids': []
}

# Invalid POI (keys correspond to None values)
poi_create_invalid_none = {
    'name': None,
    'date': None,
    'description': None,
    'map_year': None,
    'x_coord': None,
    'y_coord': None,
    'links': None,
    'media': None,
    'story_ids': None
}

map_year_invalid = 0
story_id_invalid = 0
poi_id_invalid = 0

os.environ['POI_ID'] = '1'

class POITests(unittest.TestCase):

    def test1_1_create_poi(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_create_complete)
        response = r.json()
        self.assertEqual(response['code'], 201)
        poi = response['result']['poi']
        for key in poi_create_complete:
            # Date in response is a date object, while date in json is just a string
            # self.assertEqual(response['result']['poi']['date'], poi_create_complete['date'])
            if key not in ['date', 'links', 'media', 'story_ids']:
                self.assertEqual(poi[key], poi_create_complete[key])
            elif key == 'links':
                for j in range(len(poi_create_complete[key])):
                    self.assertEqual(poi[key][j]['link_url'], poi_create_complete[key][j]['link_url'])
                    self.assertEqual(poi[key][j]['display_name'], poi_create_complete[key][j]['display_name'])
            elif key == 'media':
                for j in range(len(poi_create_complete[key])):
                    self.assertEqual(poi[key][j]['content_url'], poi_create_complete[key][j]['content_url'])
                    self.assertEqual(poi[key][j]['caption'], poi_create_complete[key][j]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_create_complete['story_ids']))
        os.environ['POI_ID'] = str(response['result']['poi']['_id'])

    def test1_2_get_poi_by_id(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        self.assertEqual(response['code'], 200)
        poi = response['result']['poi']
        self.assertEqual(poi['_id'], poi_id)
        for key in poi_create_complete:
            # Date in response is a date object, while date in json is just a string
            # self.assertEqual(response['result']['poi']['date'], poi_create_complete['date'])
            if key not in ['date', 'links', 'media', 'story_ids']:
                self.assertEqual(poi[key], poi_create_complete[key])
            elif key == 'links':
                for curr_link in range(len(poi_create_complete[key])):
                    self.assertEqual(poi[key][curr_link]['link_url'], poi_create_complete[key][curr_link]['link_url'])
                    self.assertEqual(poi[key][curr_link]['display_name'], poi_create_complete[key][curr_link]['display_name'])
            elif key == 'media':
                for curr_media in range(len(poi_create_complete[key])):
                    self.assertEqual(poi[key][curr_media]['content_url'], poi_create_complete[key][curr_media]['content_url'])
                    self.assertEqual(poi[key][curr_media]['caption'], poi_create_complete[key][curr_media]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_create_complete['story_ids']))

    def test1_3_get_pois_by_map_year(self):
        map_year = poi_create_complete['map_year']
        r = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        response = r.json()
        self.assertEqual(response['code'], 200)
        for curr_poi in response['result']['pois']:
            self.assertEqual(curr_poi['map_year'], map_year)

    def test1_4_get_pois_by_story_id(self):
        story_ids = poi_create_complete['story_ids']
        for curr_story_id in story_ids:
            r = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(curr_story_id))
            response = r.json()
            self.assertEqual(response['code'], 200)
            # Determine if the POI we previously created is included
            # in the list of POIs returned after we get request based on story_ids
            poi = next((poi for poi in response['result']['pois'] if poi['name'] == poi_create_complete['name']), None)
            self.assertIsNotNone(poi)

    def test1_5_update_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_update_complete)
        response = r.json()
        self.assertEqual(response['code'], 200)
        poi = response['result']['poi']
        for key in poi_update_complete:
            # Date in response is a date object, while date in json is just a string
            # self.assertEqual(response['result']['poi']['date'], poi_create_complete['date'])
            if key not in ['date', 'links', 'media', 'story_ids']:
                self.assertEqual(poi[key], poi_update_complete[key])
            elif key == 'links':
                for j in range(len(poi_update_complete[key])):
                    self.assertEqual(poi[key][j]['link_url'], poi_update_complete[key][j]['link_url'])
                    self.assertEqual(poi[key][j]['display_name'], poi_update_complete[key][j]['display_name'])
            elif key == 'media':
                for j in range(len(poi_update_complete[key])):
                    self.assertEqual(poi[key][j]['content_url'], poi_update_complete[key][j]['content_url'])
                    self.assertEqual(poi[key][j]['caption'], poi_update_complete[key][j]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_update_complete['story_ids']))

    def test1_6_update_none(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_update_none)
        response = r.json()
        # Successfully updates nothing
        self.assertEqual(response['code'], 200)
        # Make a get request, and then compare to poi_update_complete
        # This ensures that the put request did not change something and erronously return a 200 status code.
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        poi = response['result']['poi']
        for key in poi_update_complete:
            # Date in response is a date object, while date in json is just a string
            # self.assertEqual(response['result']['poi']['date'], poi_create_complete['date'])
            if key not in ['date', 'links', 'media', 'story_ids']:
                self.assertEqual(poi[key], poi_update_complete[key])
            elif key == 'links':
                for j in range(len(poi_update_complete[key])):
                    self.assertEqual(poi[key][j]['link_url'], poi_update_complete[key][j]['link_url'])
                    self.assertEqual(poi[key][j]['display_name'], poi_update_complete[key][j]['display_name'])
            elif key == 'media':
                for j in range(len(poi_update_complete[key])):
                    self.assertEqual(poi[key][j]['content_url'], poi_update_complete[key][j]['content_url'])
                    self.assertEqual(poi[key][j]['caption'], poi_update_complete[key][j]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_update_complete['story_ids']))

    def test1_7_delete_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        self.assertEqual(response['code'], 200)

        r2 = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response2 = r2.json()
        self.assertEqual(response2['code'], 404)

    def test2_1_invalid_create(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_create_invalid)
        response = r.json()
        self.assertEqual(response['code'], 422)

    def test2_2_invalid_get_poi_by_id(self, poi_id=0):
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id_invalid))
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test2_3_invalid_map_year(self):
        r = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year_invalid))
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test2_4_invalid_story_id(self):
        r = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(story_id_invalid))
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test2_5_invalid_delete(self):
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id_invalid))
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test3_1_invalid_create_none(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_create_invalid_none)
        response = r.json()
        self.assertEqual(response['code'], 422)
