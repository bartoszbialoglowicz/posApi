from django.test import TestCase
from django.db.utils import IntegrityError

from api import models

class ModelsTests(TestCase):

    def test_manufacturer_create(self):
        "Test creating new manufacturer"
        manufacturer = models.Manufacturer.objects.create(name="Test", country="Test")
        self.assertEqual(manufacturer.name, "Test")
        self.assertEqual(manufacturer.country, "Test")
        self.assertIn(manufacturer, models.Manufacturer.objects.filter(name="Test"))

    def test_manufacturer_not_unique_name_fail(self):
        "Test creating manufacturer with not unique name fails"
        manufacturer = models.Manufacturer.objects.create(name="Test", country="Test")
        try:
            new_manufacturer = models.Manufacturer.objects.create(name="Test", country="Test")
        except IntegrityError:
            pass