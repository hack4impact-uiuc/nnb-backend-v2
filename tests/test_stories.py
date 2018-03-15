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

story_edit_pois = {
    'poi_ids' : []
}


os.environ['STORY_ID_WITH_NO_POIS'] = '1' # this one doesn't have pois
os.environ['STORY_ID_WITH_POIS'] = '2' # this one has the pois
os.environ['POI_ID_1'] = '1'
os.environ['POI_ID_2'] = '2'

class POITests(unittest.TestCase):

    def test1_post_story(self):
        r = requests.post('http://127.0.0.1:5000/stories', json=story_with_no_pois)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['story']['story_name'], story_with_no_pois['story_name'])
        os.environ['STORY_ID_WITH_NO_POIS'] = str(response['result']['story']['_id'])

    def test2_post_story_with_pois(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi1)
        response = r.json()
        story_with_pois['poi_ids'].append(response['result']['poi']['_id'])
        os.environ['POI_ID_1'] = str(response['result']['poi']['_id'])
        poi_id_1 = int(response['result']['poi']['_id'])

        r = requests.post('http://127.0.0.1:5000/pois', json=poi2)
        response = r.json()
        story_with_pois['poi_ids'].append(response['result']['poi']['_id'])
        os.environ['POI_ID_2'] = str(response['result']['poi']['_id'])
        poi_id_2 = int(response['result']['poi']['_id'])

        r = requests.post('http://127.0.0.1:5000/stories', json=story_with_pois)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['story']['story_name'], story_with_pois['story_name'])
        os.environ['STORY_ID_WITH_POIS'] = str(response['result']['story']['_id'])
        story_id_with_pois = int(response['result']['story']['_id'])

        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id_1))
        response = r.json()
        story = next((s for s in response['result']['poi']['stories'] if s['_id'] == story_id_with_pois), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])

        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id_2))
        response = r.json()
        story = next((s for s in response['result']['poi']['stories'] if s['_id'] == story_id_with_pois), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])

    def test3_get_stories_no_params(self):
        story_id_with_no_pois = int(os.environ.get('STORY_ID_WITH_NO_POIS'))
        story_id_with_pois = int(os.environ.get('STORY_ID_WITH_POIS'))

        r = requests.get('http://127.0.0.1:5000/stories')
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story['story_name'], story_with_no_pois['story_name'])
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_pois), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])

    def test4_get_stories_by_poi(self):
        story_id_with_no_pois = int(os.environ.get('STORY_ID_WITH_NO_POIS'))
        story_id_with_pois = int(os.environ.get('STORY_ID_WITH_POIS'))
        poi_id_1 = int(os.environ.get('POI_ID_1'))
        poi_id_2 = int(os.environ.get('POI_ID_2'))

        r = requests.get('http://127.0.0.1:5000/stories?poi_id={}'.format(poi_id_1))
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_pois), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story, None)

        r = requests.get('http://127.0.0.1:5000/stories?poi_id={}'.format(poi_id_2))
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_pois), None)
        self.assertEqual(story['story_name'], story_with_pois['story_name'])
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story, None)

    def test5_put_stories_new_pois(self):
        story_id_with_no_pois = int(os.environ.get('STORY_ID_WITH_NO_POIS'))
        poi_id_1 = int(os.environ.get('POI_ID_1'))
        story_edit_pois['poi_ids'].append(poi_id_1)

        r = requests.put('http://127.0.0.1:5000/stories/{}'.format(story_id_with_no_pois), json=story_edit_pois)
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)

        r = requests.get('http://127.0.0.1:5000/stories?poi_id={}'.format(poi_id_1))
        response = r.json()
        self.assertEqual(response['code'], 200)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story['story_name'], story_with_no_pois['story_name'])

        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id_1))
        response = r.json()
        story = next((s for s in response['result']['poi']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story['story_name'], story_with_no_pois['story_name'])

    def test6_put_stories_new_name(self):
        story_id_with_no_pois = int(os.environ.get('STORY_ID_WITH_NO_POIS'))

        r = requests.put('http://127.0.0.1:5000/stories/{}'.format(story_id_with_no_pois), json=story_edit)
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)

        r = requests.get('http://127.0.0.1:5000/stories')
        response_get = r.json()
        story = next((s for s in response_get['result']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story['story_name'], story_edit['story_name'])

    def test7_put_stories_empty_payload(self):
        story_id_with_no_pois = int(os.environ.get('STORY_ID_WITH_NO_POIS'))

        r = requests.put('http://127.0.0.1:5000/stories/{}'.format(story_id_with_no_pois), json=story_empty)
        response = r.json()
        self.assertEqual(response['code'], 422)

    def test8_delete_stories(self):
        story_id_with_no_pois = int(os.environ.get('STORY_ID_WITH_NO_POIS'))
        story_id_with_pois = int(os.environ.get('STORY_ID_WITH_POIS'))
        poi_id_1 = int(os.environ.get('POI_ID_1'))
        poi_id_2 = int(os.environ.get('POI_ID_2'))

        r = requests.delete('http://127.0.0.1:5000/stories/{}'.format(story_id_with_no_pois))
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)

        r = requests.delete('http://127.0.0.1:5000/stories/{}'.format(story_id_with_pois))
        response_put = r.json()
        self.assertEqual(response_put['code'], 200)

        r = requests.get('http://127.0.0.1:5000/stories')
        response = r.json()
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_no_pois), None)
        self.assertEqual(story, None)
        story = next((s for s in response['result']['stories'] if s['_id'] == story_id_with_pois), None)
        self.assertEqual(story, None)

        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id_1))
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id_2))

    def test9_delete_nonexistent_story(self):
        r = requests.delete('http://127.0.0.1:5000/stories/{}'.format(int(0)))
        response = r.json()
        self.assertEqual(response['code'], 404)
