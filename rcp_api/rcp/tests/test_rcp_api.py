import tempfile, os
from PIL import Image
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rcp.serializers import RecipeSerializer, RecipeDetailSerializer


RCP_URL = reverse('rcp:recipe-list')


def image_upload_url(recipe_id):
    """Return image url"""
    return reverse('rcp:recipe-upload-image', args=[recipe_id])

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

    def test_partial_update_recipe(self):
        """Test updating rcp api with patch"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Curry')
        payload = {
            'title' : 'Chicken Tikka',
            'tags' : [new_tag.id]
        }
        url =detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """Test full update recipe"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            'title':'Spaghetti',
            'time_minutes':25,
            'price':40
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)


class RecipeImgUploadTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'om@test.com',
            'test@123'
        )
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_img_to_recipe(self):
        """Test uploading image to recipe"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image':ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image"""
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image':'noimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_rcp_with_tags(self):
        """Test filtering recipe with tags"""
        recipe1 = sample_recipe(user=self.user, title='Veg curry')
        recipe2 = sample_recipe(user=self.user, title='Non Veg curry')
        tag1 = sample_tag(user=self.user, name='Veg')
        tag2 = sample_tag(user=self.user, name='Non-Veg')
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag2)
        recipe3 = sample_recipe(user=self.user, title='Fish and chips')

        res = self.client.get(
            RCP_URL,
            {'tags':f'{tag1.id}, {tag2.id}'}
        )
        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_recipe_by_ingredient(self):
        """Test filtering recipe with ingredients"""
        recipe1 = sample_recipe(user=self.user, title='Veg curry')
        recipe2 = sample_recipe(user=self.user, title='Non Veg curry')
        ingredient1 = sample_ingredient(user=self.user, name='Cabbage')
        ingredient2 = sample_ingredient(user=self.user, name='Chicken')
        recipe1.ingredient.add(ingredient1)
        recipe2.ingredient.add(ingredient2)
        recipe3 = sample_recipe(user=self.user, title='Kepsa')

        res = self.client.get(
            RCP_URL,
            {'ingredient':f'{ingredient1.id}, {ingredient2.id}'}
        )
        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
