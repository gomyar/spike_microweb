
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
        setup1 = self.mock_mongo.microweb.requests.insert_one({
            'title': 'Neds Fries',
            'email': 'ned@ned.com',
            'timestamp': '2020-10-10'})

        response = self.client.get("/request/{}".format(setup1.inserted_id))

        self.assertEquals(200, response.status_code)
        self.assertEquals('Neds Fries', response.json['title'])
        self.assertEquals('ned@ned.com', response.json['email'])
        self.assertEquals('2020-10-10', response.json['timestamp'])

    def test_get_request_nonexistant(self):
        response = self.client.get("/request/5e52aa9d24c18d1fc31ce3ee")
        self.assertEquals(404, response.status_code)

    def test_delete_request(self):
        setup1 = self.mock_mongo.microweb.requests.insert_one({
            'title': 'Delete me please',
            'email': 'delete@ned.com',
            'timestamp': '2022-10-10'})

        response = self.client.delete("/request/{}".format(setup1.inserted_id))
        self.assertEquals(204, response.status_code)

        self.assertEquals(
            None, self.mock_mongo.microweb.result.find_one(setup1.inserted_id))

    def test_delete_request_nonexistant(self):
        response = self.client.delete("/request/5e52aa9d24c18d1fc31ce3ee")
        self.assertEquals(404, response.status_code)

    def test_get_all_requests(self):
        setup1 = self.mock_mongo.microweb.requests.insert_one({
            'title': 'Gerry',
            'email': 'gerry@gerry.com',
            'timestamp': '2020-11-11'})
        setup2 = self.mock_mongo.microweb.requests.insert_one({
            'title': 'Fred',
            'email': 'fred@fred.com',
            'timestamp': '2020-12-12'})

        response = self.client.get("/request")

        self.assertEquals(200, response.status_code)
        results = response.json

        self.assertEquals("Gerry", results[0]['title'])
        self.assertEquals("gerry@gerry.com", results[0]['email'])
        self.assertEquals("2020-11-11", results[0]['timestamp'])

        self.assertEquals("Fred", results[1]['title'])
        self.assertEquals("fred@fred.com", results[1]['email'])
        self.assertEquals("2020-12-12", results[1]['timestamp'])

    def test_redirect(self):
        response = self.client.get("/")

        self.assertEquals(302, response.status_code)
