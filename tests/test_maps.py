import unittest
from api.models import Map
import requests

LOCAL_MAPS_URL = 'http://127.0.0.1:5000/maps'

class MapTestCase(unittest.TestCase):
    def test_get_map_years(self):
        r = requests.get(LOCAL_MAPS_URL)
        self.assertEqual(r.status_code, 200)

    def test_create_map(self):
        new_map_json = {"map_year" : 1234, "image_url" : "https://i.ytimg.com/vi/Yj7ja6BANLM/maxresdefault.jpg"}
        r = requests.post(LOCAL_MAPS_URL, json = new_map_json)
        self.assertEqual(r.status_code, 200)
        ret_json = r.json()
        self.assertEqual(ret_json['Status'], 'Post successful')

    def test_delete_map(self):
        r = requests.delete(LOCAL_MAPS_URL + '/1')
        self.assertEqual(r.status_code, 200)
        ret_json = r.json()
        self.assertEqual(ret_json['Status'], 'Map delete successful')
