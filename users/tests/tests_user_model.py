from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='Test', password="Test", first_name="Test", last_name="Test")
        self.assertEqual(user.username, "Test")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Test")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(username='Test', password="Test", first_name="Test", last_name="Test")
        self.assertEqual(user.username, "Test")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Test")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
            
