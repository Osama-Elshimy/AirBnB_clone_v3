#!/usr/bin/python3
"""Test module for api.v1.views.cities.py"""
import json
import unittest
from api.v1.app import app
from models import storage
from models.city import City
from models.state import State


class TestCities(unittest.TestCase):
    """Test cases for the cities view module"""

    def create_state(self):
        """Create a new state for testing"""
        new_state = State(name="Cairo")
        storage.new(new_state)
        storage.save()
        return new_state.id

    def create_city(self, state_id):
        """Create a new city for testing"""
        new_city = City(name="Giza", state_id=state_id)
        storage.new(new_city)
        storage.save()
        return new_city.id

    @classmethod
    def setUpClass(cls):
        """Set up for the test cases"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test cases"""
        storage.close()

    def test_get_all(self):
        """Test city GET route"""
        s_id = self.create_state()
        self.create_city(s_id)
        response = self.client.get(f'{self.prefix}/states/{s_id}/cities')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertGreaterEqual(len(data), 1)

    def test_get_one(self):
        """Test city GET by id route"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        response = self.client.get(f'{self.prefix}/cities/{c_id}')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['name'], "Giza")
        self.assertEqual(response.status_code, 200)

    def test_get_one_404(self):
        """Test city GET by id route with 404"""
        response = self.client.get(f'{self.prefix}/cities/invalid_id')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})

    def test_create_one(self):
        """Test city POST route"""
        s_id = self.create_state()
        response = self.client.post(
            f'{self.prefix}/states/{s_id}/cities',
            data=json.dumps({"name": "Giza"}),
            content_type="application/json",
        )
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Giza")
        self.assertIn('state_id', data)
        self.assertEqual(data['state_id'], s_id)
        self.assertEqual(response.status_code, 201)

    def test_create_with_no_json(self):
        """Test city POST route with no JSON data"""
        s_id = self.create_state()
        response = self.client.post(
            f'{self.prefix}/states/{s_id}/cities',
            data="Not JSON",
            content_type="application/json",
        )
        data = response.get_json()
        self.assertEqual(data, None)
        self.assertIn("Not a JSON", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)

    def test_create_with_no_name(self):
        """Test city POST route with no name"""
        s_id = self.create_state()
        response = self.client.post(
            f'{self.prefix}/states/{s_id}/cities',
            data=json.dumps({"state_id": s_id}),
            content_type="application/json",
        )
        self.assertIn("Missing name", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)

    def test_create_with_invalid_state_id(self):
        """Test city POST route with invalid state_id"""
        response = self.client.post(
            f'{self.prefix}/states/invalid_id/cities',
            data=json.dumps({"name": "Giza"}),
            content_type="application/json",
        )
        self.assertIn("Not found", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)

    def test_update_one(self):
        """Test city PUT route"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        response = self.client.put(
            f'{self.prefix}/cities/{c_id}',
            data=json.dumps({"name": "El Sheikh Zayed"}),
            content_type="application/json",
        )
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['name'], "El Sheikh Zayed")
        self.assertEqual(response.status_code, 200)

    def test_update_with_no_json(self):
        """Test city PUT route with no JSON data"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        response = self.client.put(
            f'{self.prefix}/cities/{c_id}',
            data="Not JSON",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_with_404(self):
        """Test city PUT route with 404"""
        response = self.client.put(
            f'{self.prefix}/cities/invalid_id',
            data=json.dumps({"name": "El Sheikh Zayed"}),
            content_type="application/json",
        )
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})

    def test_delete_one(self):
        """Test city DELETE route"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        response = self.client.delete(f'{self.prefix}/cities/{c_id}')
        self.assertEqual(response.data, b'{}\n')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'{self.prefix}/cities/{c_id}')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})
        self.assertEqual(response.status_code, 404)

    def test_delete_one_404(self):
        """Test city DELETE route with 404"""
        response = self.client.delete(f'{self.prefix}/cities/invalid_id')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
