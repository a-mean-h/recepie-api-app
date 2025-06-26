from decimal import Decimal 
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse("recipe:recipe_list")

def create_recipe(user, **params):
    """create and return a sample recipe"""
    defaults = {
        "title": "Sample recipe",
        "time_minutes": 22,
        "price": Decimal("5.99"),
        "description": "Sample recipe description",
        "link": "https://example.com/recipe.pdf"
    }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

class PublicRecipeAPITest(TestCase):
    """Test Unauthorized  API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """Test authenticated Recipe API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("username@example.comn", "example123")
        self.client.force_authenticate(user=self.user)


    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializers = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.data)

    def test_recipe_list_limited_to_user(self):
        """test list of recipes is limited to authenticated user"""
        other_user = get_user_model().objects.create_user("otherusername@example.com", "othepass123")
        create_recipe(user=other_user)
        create_recipe(user = self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
        