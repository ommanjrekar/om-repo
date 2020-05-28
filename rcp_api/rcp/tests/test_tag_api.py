from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Recipe
from rcp.serializers import TagSerializers


TAG_URL = reverse('rcp:tag-list')


class PublicTagsAPI(TestCase):
    """Test that publicly available api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrievng tags"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPI(TestCase):
    """Test the authorized user"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test@123',
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)


    def test_retrieve_tags(self):
        """Test that retrieves tags for authenticated users"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Desert')
        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializers(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_tags_limited_to_user(self):
        """Test that tags are limited to logged in users"""
        user2 = get_user_model().objects.create_user(
            'om@india.com',
            'test@123'
        )
        Tag.objects.create(user=user2, name='Frootie')
        tag = Tag.objects.create(user=self.user, name='Comfort food')

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        """Test that create tag successful"""
        payload = {'name':'Test tag'}
        self.client.post(TAG_URL, payload)

        exist = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exist)

    def test_create_tag_incalid(self):
        """Test creating tag with invalid payload"""
        payload = {'name':''}
        res = self.client.post(TAG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tag_assigned_to_recipe(self):
        """Test retrieving tag assigned to recipe"""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Bread Sandwich',
            time_minutes=10,
            price=25,
            user=self.user
        )
        recipe.tags.add(tag1)
        res = self.client.get(TAG_URL, {'assigned_only':1})

        serializer1 = TagSerializers(tag1)
        serializer2 = TagSerializers(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)