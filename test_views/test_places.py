#!/usr/bin/python3
"""Test module for api/v1/views/places.py"""
import json
import unittest
from api.v1.app import app
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models import storage, storage_type


class TestPlaces(unittest.TestCase):
    """Test class for Place views"""

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

    def create_place(self, user_id, city_id):
        """Create a new place for testing"""
        new_place = Place(
            name="Pyramids Heights",
            user_id=user_id,
            city_id=city_id,
            max_guest=6,
            number_rooms=3,
            number_bathrooms=2,
            price_by_night=100,
        )
        storage.new(new_place)
        storage.save()
        return new_place.id

    def create_user(self):
        """Create a new user for testing"""
        new_user = User(email="abc@13", password="123")
        storage.new(new_user)
        storage.save()
        return new_user.id

    @classmethod
    def setUpClass(cls):
        """Setup for the test"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Teardown for the test"""
        storage.close()

    @unittest.skipIf(storage_type != 'db', "Skip for non-DB storage")
    def test_get_all(self):
        """Test get all places"""
        c_id = self.create_city(self.create_state())
        self.create_place(self.create_user(), c_id)
        response = self.client.get(f'{self.prefix}/cities/{c_id}/places')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_one(self):
        """Test get one place"""
        c_id = self.create_city(self.create_state())
        p_id = self.create_place(self.create_user(), c_id)
        response = self.client.get(f'{self.prefix}/places/{p_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Pyramids Heights")

    def test_get_404(self):
        """Test get place with 404"""
        response = self.client.get(f'{self.prefix}/places/invalid_id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})

    def test_create(self):
        """Test create place"""
        c_id = self.create_city(self.create_state())
        u_id = self.create_user()
        response = self.client.post(
            f'{self.prefix}/cities/{c_id}/places',
            data=json.dumps(
                {
                    "user_id": u_id,
                    "name": "Porto Marina",
                    "max_guest": 6,
                    "number_rooms": 3,
                    "number_bathrooms": 2,
                    "price_by_night": 100,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Porto Marina")

    def test_create_with_no_json(self):
        """Test create place with no JSON"""
        c_id = self.create_city(self.create_state())
        response = self.client.post(
            f'{self.prefix}/cities/{c_id}/places',
            data="Not JSON",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not a JSON", response.data.decode('utf-8'))

    def test_create_with_no_user_id(self):
        """Test create place with no user_id"""
        c_id = self.create_city(self.create_state())
        response = self.client.post(
            f'{self.prefix}/cities/{c_id}/places',
            data=json.dumps({"name": "Porto Marina"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing user_id", response.data.decode('utf-8'))

    def test_create_with_invalid_user_id(self):
        """Test create place with invalid user_id"""
        c_id = self.create_city(self.create_state())
        response = self.client.post(
            f'{self.prefix}/cities/{c_id}/places',
            data=json.dumps({"user_id": "invalid_id"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", response.data.decode('utf-8'))

    def test_create_with_no_name(self):
        """Test create place with no name"""
        c_id = self.create_city(self.create_state())
        response = self.client.post(
            f'{self.prefix}/cities/{c_id}/places',
            data=json.dumps({"user_id": self.create_user()}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing name", response.data.decode('utf-8'))

    def test_update(self):
        """Test update place"""
        c_id = self.create_city(self.create_state())
        p_id = self.create_place(self.create_user(), c_id)
        response = self.client.put(
            f'{self.prefix}/places/{p_id}',
            data=json.dumps({"name": "Bell Village"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Bell Village")

    def test_update_with_no_json(self):
        """Test update place with no JSON"""
        c_id = self.create_city(self.create_state())
        p_id = self.create_place(self.create_user(), c_id)
        response = self.client.put(
            f'{self.prefix}/places/{p_id}',
            data="Not JSON",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not a JSON", response.data.decode('utf-8'))

    def test_update_404(self):
        """Test update place with 404"""
        response = self.client.put(
            f'{self.prefix}/places/invalid_id',
            data=json.dumps({"name": "Bell Village"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})

    def test_update_with_empty_json(self):
        """Test update place with empty JSON"""
        c_id = self.create_city(self.create_state())
        p_id = self.create_place(self.create_user(), c_id)
        response = self.client.put(
            f'{self.prefix}/places/{p_id}',
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Pyramids Heights")

    def test_delete(self):
        """Test delete place"""
        c_id = self.create_city(self.create_state())
        p_id = self.create_place(self.create_user(), c_id)
        response = self.client.delete(f'{self.prefix}/places/{p_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {})
        response = self.client.get(f'{self.prefix}/places/{p_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_404(self):
        """Test delete place with 404"""
        response = self.client.delete(f'{self.prefix}/places/invalid_id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})


if __name__ == "__main__":
    unittest.main()
