#!/usr/bin/python3
"""Test module for api.v1.views.index"""
import json
import unittest
from api.v1.app import app

table_names = ('amenities', 'cities', 'places', 'reviews', 'states', 'users')


class TestIndex(unittest.TestCase):
    """Test API index endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up for the test cases"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    def test_status(self):
        """Test API status"""
        response = self.client.get(f'{self.prefix}/status')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {'status': 'OK'})

    def test_stats(self):
        """Test API stats"""
        response = self.client.get(f'{self.prefix}/stats')
        data = json.loads(response.data.decode('utf-8'))
        for k in table_names:
            self.assertTrue(
                k in data, f"Expected key {k} not in the response data"
            )
            v = data[k]
            self.assertIsInstance(v, int)
            self.assertTrue(v >= 0)

    def test_404(self):
        """Test API 404 response"""
        response = self.client.get(f'{self.prefix}/invalid_route')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
