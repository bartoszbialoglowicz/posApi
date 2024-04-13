from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from api import models, serializers

PRODUCT_URL = reverse('api:product-list')

def create_product(**params):
    return models.Product.objects.create(**params)

def create_manufacturer(**params):
    return models.Manufacturer.objects.create(**params)

class PublicApiTests(TestCase):
    """Tests for unauthorized API calls"""

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_access(self):
        """Test access to product list without authentication fails"""
        response = self.client.get(PRODUCT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    """Tests for authorized API calls"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="TestPassword!",
            first_name="TestFirstName",
            last_name="TestLastName"
        )
        
        self.client.force_authenticate(self.user)
        self.manufacturer = create_manufacturer(name="Test", country="Test")

    def test_get_product_list(self):
        """Tests retrieving a list of products"""
        p1 = create_product(
            name="test",
            price=10,
            manufacturer=self.manufacturer
        )
        p2 = create_product(
            name="test2",
            price=2,
            manufacturer=self.manufacturer
        )

        response = self.client.get(PRODUCT_URL)
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_create_new_product(self):
        """Test creating a new product instance"""
        payload = {
            "name": "Test",
            "price": 1,
            "manufacturer": self.manufacturer
        }

        response = self.client.post(
            PRODUCT_URL,
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)