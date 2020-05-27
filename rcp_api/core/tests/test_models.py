from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from core import models

def sample_user(email='om@test.com', password='test@123'):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_create_user_with_email(self):
        """Test for create user with email success"""
        email = 'om@india.com'
        password = 'india@11'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_normalize_email(self):
        """Normalise email"""
        email = 'om@INDIA.com'
        user = get_user_model().objects.create_user(email, 'test@123')

        self.assertEqual(user.email, email.lower())


    def test_email_validate(self):
        """Test for a valid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@123')


    def test_create_superuser(self):
        """Test to create superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag str representation"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test for ingredient model str represntation"""
        ing = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ing), ing.name)


    def test_recipe_str(self):
        """Test recipe str representation"""
        rcp =models.Recipe.objects.create(
            user=sample_user(),
            title='Tandoori Paneer',
            time_minutes=10,
            price=180,
        )

        self.assertEqual(str(rcp), rcp.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)