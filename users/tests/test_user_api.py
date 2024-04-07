from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create_user')
TOKEN_PAIR_URL = reverse('users:token_obtain_pair')


def create_user(**payload):
    return get_user_model().objects.create_user(**payload)


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.initial_payload = {
            'username': 'TestUser',
            'password': 'TestPassword!',
            'first_name': 'Test',
            'last_name': 'Test'
        }

    def test_create_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = self.initial_payload

        response = self.client.post(
            CREATE_USER_URL,
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_already_exists(self):
        "Test creating user that already exists fails"
        payload = self.initial_payload

        create_user(**payload)

        response = self.client.post(
            CREATE_USER_URL,
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creating user with too short password fails"""
        payload = self.initial_payload
        payload['password'] = 'TestPas'

        response = self.client.post(
            CREATE_USER_URL,
            payload
        )

        user_exists = get_user_model().objects.filter(username=payload['username']).exists()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_user_blank_first_name(self):
        """Test creating user with blank first_name field fails"""
        payload = self.initial_payload
        payload['first_name'] = ''

        response = self.client.post(
            CREATE_USER_URL,
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_blank_username(self):
        """Test creating user with blank username field fails"""
        payload = self.initial_payload
        payload['username'] = ''

        response = self.client.post(
            CREATE_USER_URL,
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_for_user(self):
        """Test creating token pair for user"""
        payload = self.initial_payload
        create_user(**payload)
        
        response = self.client.post(
            TOKEN_PAIR_URL,
            payload
        )

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)     
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_credentials(self):
        """Test token is not created if invalid credentials were provided"""
        payload = self.initial_payload
        create_user(**payload)
        payload['password'] = 'invalid'
    
        response = self.client.post(
            TOKEN_PAIR_URL,
            payload
        )

        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_token_no_user(self):
        """Test token is not created when provided user does not exist"""
        payload = self.initial_payload

        response = self.client.post(
            TOKEN_PAIR_URL,
            payload
        )

        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    