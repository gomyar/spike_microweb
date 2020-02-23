
import unittest
from freezegun import freeze_time

from microweb.app import app
from mongomock import MongoClient
from bson.objectid import ObjectId


class MicrowebTest(unittest.TestCase):
    def setUp(self):
        self.mock_mongo = MongoClient()
        app.config['mongo'] = self.mock_mongo
        self.client = app.test_client()

    def test_get(self):
        response = self.client.get('/')
        self.assertTrue('Hello, World' in response.data.decode())

    @freeze_time('2019-01-01')
    def test_request(self):
        response = self.client.post(
            '/request', json={
                "email": "bob@bob.com", "title": "Bobs Burgers"})
        self.assertEquals(201, response.status_code)
        self.assertEquals('bob@bob.com', response.json['email'])
        self.assertEquals('2019-01-01T00:00:00', response.json['timestamp'])
        self.assertEquals('Bobs Burgers', response.json['title'])

        document = self.mock_mongo.microweb.requests.find_one(
            {'_id': ObjectId(response.json['id'])})
        self.assertEquals('Bobs Burgers', document['title'])

    def test_get_request(self):
        result = self.mock_mongo.microweb.requests.insert_one({
            'title': 'Neds Fries',
            'email': 'ned@ned.com',
            'timestamp': '2020-10-10'})
        response = self.client.get("/request/{}".format(result.inserted_id))
        self.assertEquals(200, response.status_code)
        self.assertEquals('Neds Fries', response.json['title'])
        self.assertEquals('ned@ned.com', response.json['email'])
        self.assertEquals('2020-10-10', response.json['timestamp'])

    def test_get_request_nonexistant(self):
        response = self.client.get("/request/5e52aa9d24c18d1fc31ce3ee")
        self.assertEquals(404, response.status_code)
