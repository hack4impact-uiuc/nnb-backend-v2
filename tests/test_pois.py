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

poi = {
          'name': 'Himalayan Chimney',
          'date': 'Date(2018, 2, 27)',
          'description': 'Yum',
          'map_year': 2018,
          'x_coord': 12,
          'y_coord': 43,
          'links': [
            {
             '_id': 43,
              'link_url': 'http://fb.com',
              'display_name': 'Facebook'
            }
          ],
          'media': [
            {
              '_id': 41,
              'content_url': 'http://images.com/llama.jpg',
              'caption': 'The Llama in its natural habitat'
            }
          ],
          'stories': [
            {
              '_id': 21,
              'story_name': 'Angad Goes to Wisconsin',
            },
            {
              '_id': 22,
              'story_name': 'Alvin Gets Lost in Taiwan',
            }
          ]
      }

poi_edit = {
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

poi_edit2 = {
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

map_year = 2018
story_id = 2
os.environ['POI_ID'] = '1' #initialize POI_ID as environment variable 

class POITests(unittest.TestCase):

    def test1_create_poi(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_edit)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['poi']['name'], poi_edit['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit2['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit['description'])
        self.assertEqual(response['result']['poi']['map_year'], poi_edit['map_year'])
        self.assertEqual(response['result']['poi']['x_coord'], poi_edit['x_coord'])
        self.assertEqual(response['result']['poi']['y_coord'], poi_edit['y_coord'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit['links'][i]['display_name'])
        for j in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][j]['content_url'], poi_edit['media'][j]['content_url'])
            self.assertEqual(response['result']['poi']['media'][j]['caption'], poi_edit['media'][j]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit['story_ids']))
        os.environ['POI_ID'] = str(response['result']['poi']['_id'])

    def test2_get_poi_by_id(self, poi_id=0):
        if poi_id == 0:
            poi_id = int(os.environ.get('POI_ID'))
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['result']['poi']['_id'], poi_id)
        query_response = POI.query.get(poi_id)
        self.assertEqual(response['result']['poi']['name'], query_response.name)
        # self.assertEqual(response['result']['poi']['date'], query_response.date)
        self.assertEqual(response['result']['poi']['description'], query_response.description)
        self.assertEqual(response['result']['poi']['map_year'], query_response.map_year)
        self.assertEqual(response['result']['poi']['x_coord'], query_response.x_coord)
        self.assertEqual(response['result']['poi']['y_coord'], query_response.y_coord)

        #Account for time zones (see above commented out line)
        #Future Testing needed for links, media, stories (would require several loops based on json response)

    def test3_get_pois(self):
        r1 = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        r2 = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(story_id))
        response1 = r1.json()
        response2 = r2.json()
        #map_year
        self.assertEqual(response1['code'], 200)
        for i in response1['result']['pois']:
            self.test2_get_poi_by_id(poi_id = i['_id'])
            self.assertEqual(i['map_year'], map_year)
        # story_id
        self.assertEqual(response2['code'], 200)
        for i in response2['result']['pois']:
            stories_by_poi_id = StoryPOI.query.filter(StoryPOI.poi_id == i['_id'])
            story_ids1 = [j.to_dict()['story_id'] for j in stories_by_poi_id]
            story_ids2 = [k['_id'] for k in i['stories']]
            self.assertEqual(sorted(story_ids1), sorted(story_ids2))

    def test4_update_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_edit2)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['poi']['name'], poi_edit2['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit2['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit2['description'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit2['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit2['links'][i]['display_name'])
        for i in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][i]['content_url'], poi_edit2['media'][i]['content_url'])
            self.assertEqual(response['result']['poi']['media'][i]['caption'], poi_edit2['media'][i]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit2['story_ids']))

    def test5_delete_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id))
        response = r.json()
        self.assertEqual(response['code'], 200)
        POI_query = POI.query.get(poi_id)
        Media_query = Media.query.filter(Media.poi_id == poi_id)
        Link_query = Link.query.filter(Link.poi_id == poi_id)
        StoryPOI_query = StoryPOI.query.filter(StoryPOI.poi_id == poi_id)
        self.assertEqual(POI_query, None)
        self.assertEqual(Media_query.count(), 0)
        self.assertEqual(Link_query.count(), 0)
        self.assertEqual(StoryPOI_query.count(), 0)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(POITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
