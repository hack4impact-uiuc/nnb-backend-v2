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
    'date': '2018-08-03',
    'description': 'Hot',
    'map_year': 2018,
    'x_coord': 50,
    'y_coord': 82
}

story_with_no_pois = {
    'story_name' : 'Jeffy Discovers the Dark side of the Moon'
}

story_with_pois = {
    'story_name' : 'Angad Goes to Wisconsin',
    'poi_ids' : []
}

story_edit = {
      'story_name': 'Time for Hugs4Infants'
}

story_empty = {

}


os.environ['STORY_ID_1'] = '1' # this one doesn't have pois
os.environ['STORY_ID_2'] = '2' # this one has the pois
os.environ['POI_ID_1'] = '1'
os.environ['POI_ID_2'] = '2'

class POITests(unittest.TestCase):

    def test1_post_story(self):
        r = requests.post('http://127.0.0.1:5000/stories', json=story_with_no_pois)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['story']['story_name'], story_with_no_pois['story_name'])
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
        # GET with no parameters
        story_id_1 = int(os.environ.get('STORY_ID_1'))
        story_id_2 = int(os.environ.get('STORY_ID_2'))
        r = requests.get('http://127.0.0.1:5000/stories')
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_1), None)
        self.assertEqual(story['story_name'], story_with_no_pois['story_name'])
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_2), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])

    def test4_get_stories(self):
        # GET with poi_id parameter
        story_id_2 = int(os.environ.get('STORY_ID_2'))
        poi_id_1 = int(os.environ.get('POI_ID_1'))
        poi_id_2 = int(os.environ.get('POI_ID_2'))
        r = requests.get('http://127.0.0.1:5000/stories?poi_id={}'.format(poi_id_1))
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_2), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])
        r = requests.get('http://127.0.0.1:5000/stories?poi_id={}'.format(poi_id_2))
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_2), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])

    def test5_put_stories(self):
        # PUT with new story name
        story_id_1 = int(os.environ.get('STORY_ID_1'))
        r = requests.put('http://127.0.0.1:5000/stories/{}'.format(story_id_1), json=story_edit)
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)
        r = requests.get('http://127.0.0.1:5000/stories')
        response_get = r.json()
        story = next((s for s in response_get['result']['stories'] if s['_id'] == story_id_1), None)
        self.assertEqual(story['story_name'], story_edit['story_name'])

    def test6_put_stories(self):
        # PUT with blank payload
        story_id_1 = int(os.environ.get('STORY_ID_1'))
        r = requests.put('http://127.0.0.1:5000/stories/{}'.format(story_id_1), json=story_empty)
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)
        r = requests.get('http://127.0.0.1:5000/stories')
        response_get = r.json()
        story = next((s for s in response_get['result']['stories'] if s['_id'] == story_id_1), None)
        self.assertEqual(story['story_name'], story_edit['story_name'])

    def test7_delete_stories(self):
        story_id_1 = int(os.environ.get('STORY_ID_1'))
        story_id_2 = int(os.environ.get('STORY_ID_2'))
        r = requests.delete('http://127.0.0.1:5000/stories/{}'.format(story_id_1))
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)
        r = requests.delete('http://127.0.0.1:5000/stories/{}'.format(story_id_2))
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)
        r = requests.get('http://127.0.0.1:5000/stories')
        response = r.json()
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_1), None)
        self.assertEqual(story, None)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_2), None)
        self.assertEqual(story, None)
