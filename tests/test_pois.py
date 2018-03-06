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

poi_id = 1
map_year = 2018
story_id = 2

class POITests(unittest.TestCase):

    def test_get_pois(self):
        r1 = requests.get('http://127.0.0.1:5000/pois?map_year={}'.format(map_year))
        r2 = requests.get('http://127.0.0.1:5000/pois?story_id={}'.format(story_id))
        response1 = r1.json()
        response2 = r2.json()
        #map_year
        self.assertEqual(response1['code'], 200)
        for i in response1['result']['pois']:
            self.test_get_poi_by_id(poi_id = i['_id'])
            self.assertEqual(i['map_year'], map_year)
        # story_id
        self.assertEqual(response2['code'], 200)
        for i in response2['result']['pois']:
            stories_by_poi_id = StoryPOI.query.filter(StoryPOI.poi_id == i['_id'])
            story_ids1 = [j.to_dict()['story_id'] for j in stories_by_poi_id]
            story_ids2 = [k['_id'] for k in i['stories']]
            self.assertEqual(sorted(story_ids1), sorted(story_ids2))

    def test_get_poi_by_id(self, poi_id = poi_id):
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

    def test_create_poi(self):
        

    def test_update_poi(self):
        pass

    def test_delete_poi(self):
        pass

    # def test_add_poi(self):
    #     r = requests.post('http://127.0.0.1:5000/pois', data=json.dumps(poi_add_json))
    #     self.assertEqual(r.status_code,200)
    #     json_dict = r.json()
    #     print(json_dict)
    #     self.assertEqual(json_dict["status"], "success")
    #
    # def test_add_multiple_poi(self):
    #
    #     r = requests.post('http://127.0.0.1:5000/pois', data=json.dumps(poi_add_json))
    #     r = requests.post('http://127.0.0.1:5000/pois', data=json.dumps(poi_add_json))
    #
    #
    # def test_get_poi_by_id(self):
    #     r = requests.get('http://127.0.0.1:5000/pois/60')
    #     self.assertEqual(r.status_code,200)
    #     json_dict = r.json()
    #     poi = PointsOfInterest.query.get(60)
    #     print("POI name")
    #     print(poi)
    #     name = poi.name
    #     print(name)
    #     self.assertEqual(json_dict['data'][0]["name"], name)
    #
    # def test_delete_poi(self):
    #     r2 = requests.post('http://127.0.0.1:5000/pois', data=json.dumps(poi_add_json))
    #     self.assertEqual(r.status_code,200)
    #     json_dict = r2.json()
    #     ID = json_dict['data']['id']
    #     r = requests.delete('http://127.0.0.1:5000/pois/' + ID)
    #     self.assertEqual(r.status_code,200)
    #     json_dict = r.json()
    #     self.assertEqual(json_dict['status'], "success")
    # def get_poi_with_id(self):


# app = Flask(__name__)
# with app.app_context():
#     r = requests.post(url = "http://127.0.0.1:5000/",params=jsonify({'username':'admin', 'password': 'admin'}))

# class BasicTests(unittest.TestCase):
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nbb:password@127.0.0.1:5432/nbb_db'
#         self.app = app.test_client()

#         db.drop_all()
#         db.create_all()

#         # Disable sending emails during unit testing
#         # mail.init_app(app)
#         self.assertEqual(app.debug, False)

#     # executed after each test
#     def tearDown(self):
#         pass



#     def test_main_page(self):
#         response = self.app.get('/', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         result = self.app.get('/pois')
#         client = app.test_client()
#         # client.post('/signup',
#         #     jsonify({'username':'admin', 'password': 'admin'})
#         # )
#         # client.post('/signup', data=dict(
#         #     username="admin",
#         #     password="admin"
#         # ), follow_redirects=True)

#     def register(self, username, password):
#         return "HI"
#         return self.app.post(
#         '/signup',
#         data=dict(username=username, password=password),
#         follow_redirects=True
#     )

#     def login(self, username, password):
#         return self.app.post(
#             '/login',
#             data=dict(username=username, password=password),
#             follow_redirects=True
#         )

#     def logout(self):
#         return self.app.get(
#             '/logout',
#             follow_redirects=True
#         )

#     def test_valid_user_registration(self):
#         response = self.register("patkennedy79@gmail.com", "FlaskIsAwesome")
#         # self.assertEqual(response.status_code, 200)
#         # self.assertIn(b'Thanks for registering!', response.data)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(POITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
