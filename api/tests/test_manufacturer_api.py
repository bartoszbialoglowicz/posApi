from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api import models, serializers


MANUFACTURERS_URL = reverse('api:manufacturer-list')


def create_manufacturer(name, country):
    return models.Manufacturer.objects.create(name=name, country=country)

def get_detail_url(id):
    return reverse('api:manufacturer-detail', kwargs={'pk': id})


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
    
    def test_create_manufacturer(self):
        """Test creating a new manufacturer instance"""
        payload = {
            "name": "test",
            "country": "test"
        }
        
        response = self.client.post(
            MANUFACTURERS_URL,
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        manufacturer = models.Manufacturer.objects.get(id=response.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(manufacturer, key))
    
    def test_update_manufacturer(self):
        """Test partial update a manufacturer instance"""
        payload = {
            "name": "test",
            "country": "test"
        }
        payload2 = {
            "name": "TestNew"
        }
        manufacturer = create_manufacturer(**payload)
        url = get_detail_url(manufacturer.pk)

        response = self.client.patch(
            url,
            payload2,
            format='json'
        )

        manufacturer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload2["name"], manufacturer.name)

    def test_full_update_manufacturer(self):
        """Test updating a whole manufacturer instance"""
        payload = {
            "name": "test1",
            "country": "test1"
        }
        payload2 = {
            "name": "Test2",
            "country": "Test2"
        }
        manufacturer = create_manufacturer(**payload)
        url = get_detail_url(manufacturer.pk)

        response = self.client.put(
            url,
            payload2,
            format="json"
        )

        manufacturer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload2["country"], manufacturer.country)
        self.assertEqual(payload2["name"], manufacturer.name)