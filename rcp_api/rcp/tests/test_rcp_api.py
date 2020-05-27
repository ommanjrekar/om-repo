from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rcp.serializers import RecipeSerializer, RecipeDetailSerializer


RCP_URL = reverse('rcp:recipe-list')

def detail_url(recipe_id):
    """Recipe detail url"""
    return reverse('rcp:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main course'):
    """Returns sample tags"""
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='Turmeric'):
    """Returns sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create and return new recipe"""
    defaults = {
        'title':'Sample recipe',
        'time_minutes':10,
        'price':50
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRcpApi(TestCase):
    """Test unauthenticated rcp api access"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication required"""
        res = self.client.get(RCP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRcpApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test@123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_rcp(self):
        """Test that retrieve recipe to authenticated user"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RCP_URL)

        recipe = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_rcp_limited_to_user(self):
        """Test that recipe limited to only authenticated users """
        user2 = get_user_model().objects.create_user(
            'om@test.com',
            'test@123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RCP_URL)

        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test detail view of recipe"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredient.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating basic recipe"""
        payload = {
            'title':'Choclate cake',
            'time_minutes':30,
            'price':100
        }

        res = self.client.post(RCP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Test create recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Desert')
        payload = {
            'title':'Avocardo Chese cake',
            'tags':[tag1.id, tag2.id],
            'time_minutes':40,
            'price':190
        }
        res = self.client.post(RCP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredient(self):
        """Test create recipe with igredient"""
        ingredient1 = sample_ingredient(user=self.user, name='Ginger')
        ingredient2 = sample_ingredient(user=self.user, name='Salt')
        payload = {
            'title':'Prawn Curry',
            'ingredient':[ingredient1.id, ingredient2.id],
            'time_minutes':30,
            'price':100
        }
        res = self.client.post(RCP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredient = recipe.ingredient.all()
        self.assertEqual(ingredient.count(), 2)
        self.assertIn(ingredient1, ingredient)
        self.assertIn(ingredient2, ingredient)
