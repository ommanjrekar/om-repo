from django.test import TestCase
from ..models import Puppy

class PuppyTest(TestCase):
    """Test for puppy model"""
    def setUp(self):
        Puppy.objects.create(
            name='Kaliya', age=5, breed='Stray', color='Black'
        )
        Puppy.objects.create(
            name='Wadi', age=3, breed='Stray', color='Brown'
        )

    def test_puppy_breed(self):
        puppy_kaliya = Puppy.objects.get(name='Kaliya')
        puppy_wadi = Puppy.objects.get(name='Wadi')
        self.assertEqual(
            puppy_kaliya.get_breed(), "Kaliya belongs to Stray breed."
        )
        self.assertEqual(
            puppy_wadi.get_breed(), "Wadi belongs to Stray breed."
        )