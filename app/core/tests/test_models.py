from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


class ModelTest(TestCase):
    """
    test models
    """
    def test_create_user(self):
        """
        test creating user with an email is successful
        """
        email = "test@example.com"
        password = "password123"
        user = get_user_model().objects.create_user(
            email=email, password=password
            )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test email is normalized for new user
        """
        sample_emails = [
            ["test1@Example.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@Example.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"]
        ]
        for email, excepted in sample_emails:
            user = get_user_model().objects.create_user(
                email, "sample123"
            )
            self.assertEqual(user.email, excepted)

    def test_new_user_without_email_raise_error(self):
        """
        test that creating a user without an email raises a ValueError
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """
        Test creating a super user
        """
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        user = get_user_model().objects.create_user("test@example.com", "testpass123")
        recipe = models.Recipe.objects.create(
            user = user,
            title = "Sample recipe",
            price = Decimal("5.50"),
            time_minute = 20,
            description = "Sample recipe description",
        )
        self.assertEqual(str(recipe), recipe.title)