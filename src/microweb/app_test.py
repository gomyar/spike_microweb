
import unittest

from microweb.app import app


class MicrowebTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get(self):
        response = self.client.get('/')
        self.assertTrue('Hello, World' in response.data.decode())
