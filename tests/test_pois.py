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

#GOOD

poi_edit1_good = {
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

poi_edit2_good = {
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

#OK (expected to all pass)

poi_edit1_ok = {
    #This one needs EITHER map_year OR story_ids
    'name': 'Morrow Plots',
    #Technically date is not required, but frontend will automatically send in date as 1/1/mapyear
    #Otherwise there would be an error when running this test
    'date': '1856-01-01',
    'description': 'Just corn here',
    'map_year': 1856,
    'x_coord': 76,
    'y_coord': 42,
    'links': [],
    'media': [],
    'story_ids': []
}

poi_edit2_ok = {
    'name': 'Morrow Plots',
    #Technically date is not required, but frontend will automatically send in date as 1/1/mapyear
    #Otherwise there would be an error when running this test
    'date': '1856-01-01',
    'description': 'Just corn here',
    'links': [],
    'media': [],
    'story_ids': []
}

#BAD

poi_edit1_bad = {
    #Does not have name
    #Does not have description
    #Does not have map_year
    #Does not have x-coord or y-coord
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

poi_edit2_bad = {
    'name': '',
    'date': '01-01-00',
    'description': '',
    'links': [],
    'media': [],
    'story_ids': []
}

#Move to separate file

map_year = 2018
story_id = 2

map_year_bad = 10000
story_id_bad = 10000
poi_id_bad = 10000

os.environ['POI_ID'] = '1' #initialize POI_ID as environment variable

class POITests(unittest.TestCase):

    def test0_1_create_poi(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_edit1_good)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['poi']['name'], poi_edit1_good['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit1_good['description'])
        self.assertEqual(response['result']['poi']['map_year'], poi_edit1_good['map_year'])
        self.assertEqual(response['result']['poi']['x_coord'], poi_edit1_good['x_coord'])
        self.assertEqual(response['result']['poi']['y_coord'], poi_edit1_good['y_coord'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit1_good['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit1_good['links'][i]['display_name'])
        for j in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][j]['content_url'], poi_edit1_good['media'][j]['content_url'])
            self.assertEqual(response['result']['poi']['media'][j]['caption'], poi_edit1_good['media'][j]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit1_good['story_ids']))
        os.environ['POI_ID'] = str(response['result']['poi']['_id'])

    def test0_2_get_poi_by_id(self, poi_id=0):
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

    def test0_3_get_pois(self):
        r1 = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        r2 = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(story_id))
        response1 = r1.json()
        response2 = r2.json()
        #map_year
        self.assertEqual(response1['code'], 200)
        for i in response1['result']['pois']:
            self.test0_2_get_poi_by_id(poi_id = i['_id'])
            self.assertEqual(i['map_year'], map_year)
        # story_id
        self.assertEqual(response2['code'], 200)
        for i in response2['result']['pois']:
            stories_by_poi_id = StoryPOI.query.filter(StoryPOI.poi_id == i['_id'])
            story_ids1 = [j.to_dict()['story_id'] for j in stories_by_poi_id]
            story_ids2 = [k['_id'] for k in i['stories']]
            self.assertEqual(sorted(story_ids1), sorted(story_ids2))

    def test0_4_update_poi(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_edit2_good)
        response = r.json()
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['result']['poi']['name'], poi_edit2_good['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit2_good['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit2_good['description'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit2_good['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit2_good['links'][i]['display_name'])
        for i in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][i]['content_url'], poi_edit2_good['media'][i]['content_url'])
            self.assertEqual(response['result']['poi']['media'][i]['caption'], poi_edit2_good['media'][i]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit2_good['story_ids']))

    def test0_5_delete_poi(self):
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

    def test1_1_ok(self):
        r = requests.post('http://127.0.0.1:5000/pois', json=poi_edit1_ok)
        response = r.json()
        self.assertEqual(response['code'], 201)
        self.assertEqual(response['result']['poi']['name'], poi_edit1_ok['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit1_ok['description'])
        self.assertEqual(response['result']['poi']['map_year'], poi_edit1_ok['map_year'])
        self.assertEqual(response['result']['poi']['x_coord'], poi_edit1_ok['x_coord'])
        self.assertEqual(response['result']['poi']['y_coord'], poi_edit1_ok['y_coord'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit1_ok['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit1_ok['links'][i]['display_name'])
        for j in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][j]['content_url'], poi_edit1_ok['media'][j]['content_url'])
            self.assertEqual(response['result']['poi']['media'][j]['caption'], poi_edit1_ok['media'][j]['caption'])
        response_story_ids = [k['_id'] for k in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit1_ok['story_ids']))
        os.environ['POI_ID'] = str(response['result']['poi']['_id'])

    def test1_4_ok(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_edit2_ok)
        response = r.json()
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['result']['poi']['name'], poi_edit2_ok['name'])
        # self.assertEqual(response['result']['poi']['date'], poi_edit2_good['date'])
        self.assertEqual(response['result']['poi']['description'], poi_edit2_ok['description'])
        for i in range(len(response['result']['poi']['links'])):
            self.assertEqual(response['result']['poi']['links'][i]['link_url'], poi_edit2_ok['links'][i]['link_url'])
            self.assertEqual(response['result']['poi']['links'][i]['display_name'], poi_edit2_ok['links'][i]['display_name'])
        for i in range(len(response['result']['poi']['media'])):
            self.assertEqual(response['result']['poi']['media'][i]['content_url'], poi_edit2_ok['media'][i]['content_url'])
            self.assertEqual(response['result']['poi']['media'][i]['caption'], poi_edit2_ok['media'][i]['caption'])
        response_story_ids = [i['_id'] for i in response['result']['poi']['stories']]
        self.assertEqual(sorted(response_story_ids), sorted(poi_edit2_ok['story_ids']))
    #
    # #Below...2
    # #Tests that should fail or break
    # #Tests that should fail or break
    # #Tests that should fail or break
    # #Tests that should fail or break
    # #Tests that should fail or break
    # #Tests that should fail or break
    #
    def test2_1_bad(self):
        r = requests.post('http://127.0.0.1:5000/pois', json= poi_edit1_bad)
        response = r.json()
        self.assertEqual(response['code'], 422)

    def test2_2_bad(self, poi_id=0):
        # if poi_id == 0:
        #     poi_id = int(os.environ.get('POI_ID'))
        r = requests.get('http://127.0.0.1:5000/pois/{}'.format(poi_id_bad))
        response = r.json()
        self.assertEqual(response['code'], 404)
        # self.assertEqual(response['result']['poi']['_id'], poi_id_bad)
        # query_response = POI.query.get(poi_id_bad)
        # self.assertEqual(response['result']['poi']['name'], query_response.name)
        # # self.assertEqual(response['result']['poi']['date'], query_response.date)
        # self.assertEqual(response['result']['poi']['description'], query_response.description)
        # self.assertEqual(response['result']['poi']['map_year'], query_response.map_year)
        # self.assertEqual(response['result']['poi']['x_coord'], query_response.x_coord)
        # self.assertEqual(response['result']['poi']['y_coord'], query_response.y_coord)

    def test2_3_bad(self):
        r1 = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year_bad))
        r2 = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(story_id_bad))
        response1 = r1.json()
        response2 = r2.json()
        #map_year_bad
        self.assertEqual(response1['code'], 404)
        # for i in response1['result']['pois']:
        #     self.test2_get_poi_by_id(poi_id = i['_id']) #GONNA HAVE AN ISSUE HERE
        #     self.assertEqual(i['map_year'], map_year_bad)
        # story_id_bad
        self.assertEqual(response2['code'], 404)
        # for i in response2['result']['pois']:
        #     stories_by_poi_id = StoryPOI.query.filter(StoryPOI.poi_id == i['_id'])
        #     story_ids1 = [j.to_dict()['story_id'] for j in stories_by_poi_id]
        #     story_ids2 = [k['_id'] for k in i['stories']]
        #     self.assertEqual(sorted(story_ids1), sorted(story_ids2))

    def test2_4_ok(self):
        #This is ok because an empty input should still be valid.
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json=poi_edit2_bad)
        response = r.json()
        self.assertEqual(response['code'], 200)

    def test2_5_bad(self):
        # poi_id = int(os.environ.get('POI_ID'))
        r = requests.delete('http://127.0.0.1:5000/pois/{}'.format(poi_id_bad))
        response = r.json()
        self.assertEqual(response['code'], 404)
        # POI_query = POI.query.get(poi_id_bad)
        # Media_query = Media.query.filter(Media.poi_id == poi_id_bad)
        # Link_query = Link.query.filter(Link.poi_id == poi_id_bad)
        # StoryPOI_query = StoryPOI.query.filter(StoryPOI.poi_id == poi_id_bad)
        # self.assertEqual(POI_query, None)
        # self.assertEqual(Media_query.count(), 0)
        # self.assertEqual(Link_query.count(), 0)
        # self.assertEqual(StoryPOI_query.count(), 0)

    def test3_1_None(self):
        r = requests.post('http://127.0.0.1:5000/pois', json= None)
        response = r.json()
        self.assertEqual(response['code'], 404)

    def test4_4_None(self):
        poi_id = int(os.environ.get('POI_ID'))
        r = requests.put('http://127.0.0.1:5000/pois/{}'.format(poi_id), json= None)
        response = r.json()
        self.assertEqual(response['code'], 404)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(POITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
