from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestCreateUser(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test to create valid user"""
        payload = {
            'email':'om@test.com',
            'password':'test@123',
            'name':'Omkar Manjrekar',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_already_exist(self):
        """Test to check user is already exists"""
        payload = {
            'email':'om@test.com',
            'password':'test@123',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_length(self):
        """Test for password length"""
        payload = {
            'email':'om@test.com',
            'password':'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test for creating a token for user"""
        payload = {'email':'om@test.com', 'password':'test@123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalis_creds(self):
        """Test that does not create token for invalid credentials"""
        create_user(email='om@test.com', password='test@123')
        payload = {'email':'om@test.com', 'password':'wrongps'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_no_user(self):
        """Test that does not create token if user is not exists"""
        payload = {'email':'om@test.com', 'password':'wrongps'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that does not create toke if fields are missing"""
        res = self.client.post(TOKEN_URL, {'email':'one', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTest(TestCase):
    """Test API request that requires authentication"""

    def setUp(self):
        self.user = create_user(
            email='om@india.com',
            password='test@123',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieve profile for logged in users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name':self.user.name,
            'email':self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test that ensures POST method is not allowed"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """Test that patch method is allowed for signed in user"""
        payload = {'name':'new name', 'password':'newpass'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)



