import os
import unittest
from flask import jsonify
from api import app, db
from flask import Flask, request
from api.models import POI, Media, Link, Story, StoryPOI
import requests
from flask import jsonify
import json

poi1 = {
    'name': 'Himalayan Chimney',
    'date': '2018-02-02',
    'description': 'Yum',
    'map_year': 2018,
    'x_coord': 12,
    'y_coord': 43
}

poi2 = {
    'name': 'Mount Everest',
    'date': '2018-05-15',
    'description': 'Snow',
    'map_year': 2018,
    'x_coord': 15,
    'y_coord': 30
}

poi3 = {
    'name': 'Tampa Bay',
    'date': 'Date(2018, 8, 3)',
    'description': 'Hot',
    'map_year': 2018,
    'x_coord': 50,
    'y_coord': 82
}

stories = [
    {
      '_id': 21,
      'story_name': 'Angad Goes to Wisconsin',
    },
    {
      '_id': 22,
      'story_name': 'Amanda Takes her Medicine',
    },
    {
      '_id': 23,
      'story_name': 'Jeffy Goes to Fashion Show',
    },
    {
      '_id': 24,
      'story_name': 'Time for Hack4Impact',
    }
]


story_empty = {
    'story_name' : 'Jeffy Discovers the Dark side of the Moon'
}

story_with_pois = {
    'story_name' : 'Angad Goes to Wisconsin',
    'poi_ids' : []
}


os.environ['STORY_ID_1'] = '1' # this one doesn't have pois
os.environ['STORY_ID_2'] = '2' # this one has the pois
os.environ['POI_ID_1'] = '1'
os.environ['POI_ID_2'] = '2'

class POITests(unittest.TestCase):

    def test1_post_story(self):
        r = requests.post('http://127.0.0.1:5000/stories', json=story_empty)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['story']['story_name'], story_empty['story_name'])
        os.environ['STORY_ID_1'] = str(response['result']['story']['_id'])

    def test2_post_story_with_pois(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi1)
        response = r.json()
        story_with_pois['poi_ids'].append(response['result']['poi']['_id'])
        os.environ['POI_ID_1'] = str(response['result']['poi']['_id'])
        r = requests.post('http://127.0.0.1:5000/pois', json=poi2)
        response = r.json()
        story_with_pois['poi_ids'].append(response['result']['poi']['_id'])
        os.environ['POI_ID_2'] = str(response['result']['poi']['_id'])
        r = requests.post('http://127.0.0.1:5000/stories', json=story_with_pois)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['story']['story_name'], story_with_pois['story_name'])
        os.environ['STORY_ID_2'] = str(response['result']['story']['_id'])

    def test3_get_stories(self):
        story_id_1 = int(os.environ.get('STORY_ID_1'))
        story_id_2 = int(os.environ.get('STORY_ID_2'))
        poi_id_1 = int(os.environ.get('POI_ID_1'))
        # GET with no parameters
        r = requests.get('http://127.0.0.1:5000/stories')
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_1), None)
        self.assertEqual(story['story_name'], story_empty['story_name'])
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_2), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])
        # GET with poi_id parameter
        r = requests.get('http://127.0.0.1:5000/stories?poi_id={}'.format(poi_id_1))
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_2), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])
