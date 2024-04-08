from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api import models, serializers


MANUFACTURERS_URL = reverse('api:manufacturers')


def create_manufacturer(name, country):
    return models.Manufacturer.objects.create(name=name, country=country)


class PublicApiTests(TestCase):
    """Test unauthenticated manufacturer API calls"""

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_access(self):
        """Test access without authentication fails"""
        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    """Test authenticated API calls"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='TestUser',
            password='TestPassword!',
            first_name="Test",
            last_name="Test"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_manufacturers(self):
        """Test retrievig a list of manufacturers"""
        create_manufacturer("test1", "pol")
        create_manufacturer("test2", "pol")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = models.Manufacturer.objects.all()
        serializer = serializers.ManufacturerSerializer(manufacturers, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)