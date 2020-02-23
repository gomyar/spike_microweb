
import unittest
from freezegun import freeze_time

from microweb.app import app
from mongomock import MongoClient


class MicrowebTest(unittest.TestCase):
    def setUp(self):
        app.config['mongo'] = MongoClient()
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
