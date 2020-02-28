from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        email = 'om@xyz.com'
        password = '123456'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalized(self):
        '''Test the email for new user is normalised'''
        email = 'omi@XYZ.com'
        user = get_user_model().objects.create_user(email, '1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_superuser(self):
        '''create a new super user'''
        user = get_user_model().objects.create_superuser(
            'xyz@mno.com',
            '1234567'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
