#!/usr/bin/python3
"""Test module for api/v1/views/users.py"""
import json
import unittest
from models import storage
from api.v1.app import app
from models.user import User


class TestUsers(unittest.TestCase):
    """Test class for User views"""

    def create_user(self):
        """Create a new user for testing"""
        new_user = User(email="abc@123", password="123")
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

    def test_get_all(self):
        """Test user GET route"""
        self.create_user()
        response = self.client.get(f'{self.prefix}/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_one(self):
        """Test user GET by id route"""
        u_id = self.create_user()
        response = self.client.get(f'{self.prefix}/users/{u_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(u_id, response.data.decode('utf-8'))

    def test_get_404(self):
        """Test user GET by id route with 404"""
        response = self.client.get(f'{self.prefix}/users/invalid_id')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})

    def test_create(self):
        """Test user POST route"""
        response = self.client.post(
            f'{self.prefix}/users/',
            data=json.dumps({"email": "def@146", "password": "passw00rd"}),
            content_type="application/json",
        )
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertIn('email', data)
        self.assertEqual(data['email'], "def@146")

    def test_create_invalid_json(self):
        """Test user POST route with invalid JSON"""
        response = self.client.post(
            f'{self.prefix}/users/',
            data='Not JSON',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Not a JSON', response.data.decode('utf-8'))

    def test_create_no_email(self):
        """Test user POST route with no email"""
        response = self.client.post(
            f'{self.prefix}/users/',
            data=json.dumps({"password": "passw00rd"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data.decode('utf-8'))

    def test_create_no_password(self):
        """Test user POST route with no password"""
        response = self.client.post(
            f'{self.prefix}/users/',
            data=json.dumps({"email": "def@146"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data.decode('utf-8'))

    def test_update(self):
        """Test user PUT route"""
        u_id = self.create_user()
        response = self.client.put(
            f'{self.prefix}/users/{u_id}',
            data=json.dumps({"password": "new_pass"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('password', data)
        self.assertEqual(data['password'], "new_pass")

    def test_update_with_no_json(self):
        """Test user PUT route with no JSON"""
        u_id = self.create_user()
        response = self.client.put(
            f'{self.prefix}/users/{u_id}',
            data='Not JSON',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Not a JSON', response.data.decode('utf-8'))

    def test_update_with_empty_json(self):
        """Test user PUT route with empty JSON"""
        u_id = self.create_user()
        response = self.client.put(
            f'{self.prefix}/users/{u_id}',
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('email', data)
        self.assertEqual(data['email'], "abc@123")
        self.assertIn('password', data)
        self.assertEqual(data['password'], "123")

    def test_update_404(self):
        """Test user PUT route with 404"""
        response = self.client.put(
            f'{self.prefix}/users/invalid_id',
            data=json.dumps({"password": "new_pass"}),
            content_type="application/json",
        )
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """Test user DELETE route"""
        u_id = self.create_user()
        response = self.client.delete(f'{self.prefix}/users/{u_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {})
        response = self.client.get(f'{self.prefix}/users/{u_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_404(self):
        """Test user DELETE route with 404"""
        response = self.client.delete(f'{self.prefix}/users/invalid_id')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
