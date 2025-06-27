from decimal import Decimal 
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse("recipe:recipe-list")

def get_detail_url(recipe_id):
    return reverse ("recipe:recipe-detail", args=[recipe_id])

def create_recipe(user, **params):
    defaults = {
        "title": "Sample recipe",
        "time_minute": 22,
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
        other_user = get_user_model().objects.create_user("otheruser@exammple.com", "otherpass123")
        create_recipe(user=self.user)
        create_recipe(user=other_user)
        res = self.client.get(RECIPES_URL)
        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_recipe_detail(self):
        """test retrieve details of a recipe"""
        recipe = create_recipe(self.user)
        url = get_detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """test creating a recipe"""
        payload = {
            "title": "Sample Recipe",
            "time_minute": 45,
            "price": Decimal("6.99")
        }
        res = self.client.post(RECIPES_URL, payload),
        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for k,v in payload.items():
            self.assertEqual(getattr(recipe.k), v)
        self.assertEqual(recipe.user, self.user)