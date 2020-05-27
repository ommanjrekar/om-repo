from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from core.models import Ingredient
from rcp.serializers import IngredientSerializer


INGREDIENT_URL = reverse('rcp:ingredient-list')


class PublicIngredientAPI(TestCase):
    """Test pubically available ingredients"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPI(TestCase):
    """Test that ingredient can be retrieved by authorized users"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'omkar@india.com',
            'test@123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test to retrieve ing list"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENT_URL)

        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test that only ingredients for the authenticated user are retrieved"""
        user2 = get_user_model().objects.create_user(
            'user2@test.com',
            'test@123'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Chilly')
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test to create ingredient succesful"""
        payload = {'name':'Cabbage'}
        self.client.post(INGREDIENT_URL, payload)

        exist = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exist)

    def test_create_ingredient_invalid(self):
        """Invalid ingredient fails"""
        payload = {'name':''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)