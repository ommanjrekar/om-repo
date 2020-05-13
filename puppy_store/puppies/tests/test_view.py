import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..serializers import PuppySerializer
from ..models import Puppy


#initialize the APIClient
client = Client()

class GetAllPuppyTest(TestCase):
    """Test for get all puppies"""
    def setUp(self):
        Puppy.objects.create(
            name='Kaliya', age=5, breed='Stray', color='Black'
        )
        Puppy.objects.create(
            name='Wadi', age=3, breed='Stray', color='Brown'
        )
        Puppy.objects.create(
            name='Kolha', age=5, breed='Stray', color='Brown'
        )
        Puppy.objects.create(
            name='Sindhudurga', age=2, breed='Bulldog', color='White'
        )
        Puppy.objects.create(
            name='Diwankhavti', age=6, breed='Pitbull', color='Brown'
        )

    def test_get_all_puppies(self):
        #get API response
        response = client.get(reverse('get_post_puppy'))
        #get data from db
        puppies = Puppy.objects.all()
        serializer = PuppySerializer(puppies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePuppyTest(TestCase):
    """Test to get single Puppy"""
    def setUp(self):
        self.kaliya = Puppy.objects.create(
            name='Kaliya', age=5, breed='Stray', color='Black'
        )
        self.wadi = Puppy.objects.create(
            name='Wadi', age=3, breed='Stray', color='Brown'
        )
        self.kolha = Puppy.objects.create(
            name='Kolha', age=5, breed='Stray', color='Brown'
        )
        self.sindhudurga = Puppy.objects.create(
            name='Sindhudurga', age=2, breed='Bulldog', color='White'
        )
        self.diwan = Puppy.objects.create(
            name='Diwankhavti', age=6, breed='Pitbull', color='Brown'
        )

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk' : self.kaliya.pk})
        )
        puppy = Puppy.objects.get(pk=self.kaliya.pk)
        serializer = PuppySerializer(puppy)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk' : 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPuppyTest(TestCase):
    """Test for inserting new puppy"""
    def setUp(self):
        self.valid_payload = {
            'name' : 'Kaliya',
            'age' : 5,
            'breed' : 'Stray',
            'color' : 'Black',
        }

        self.invalid_payload = {
            'name' : '',
            'age' : 5,
            'breed' : 'Stray',
            'color' : 'Black',
        }

    def test_post_valid_puppy(self):
        response = client.post(
            reverse('get_post_puppy'),
            data = json.dumps(self.valid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_puppy(self):
        response = client.post(
            reverse('get_post_puppy'),
            data = json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdatePuppytest(TestCase):
    """Test for updating the puppy"""
    def setUp(self):
        self.kaliya = Puppy.objects.create(
            name = 'Kaliya', age = 3, breed = 'Stray', color = 'Black'
        )
        self.wadi = Puppy.objects.create(
            name = 'Wadi', age = 2, breed = 'Stray', color = 'Brown'
        )

        self.valid_payload = {
            'name' : 'Kaliya',
            'age' : 5,
            'breed' : 'Stray',
            'color' : 'Black'
        }
        self.invalid_payload = {
            'name' : '',
            'age' : 5,
            'breed' : 'Stray',
            'color' : 'Black'
        }

    def test_update_valid_puppy(self):
        response = client.put(
            reverse('get_delete_update_puppy', kwargs = {'pk' : self.kaliya.pk}),
            data = json.dumps(self.valid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_puppy(self):
        response = client.put(
            reverse('get_delete_update_puppy', kwargs = {'pk' : self.kaliya.pk}),
            data = json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeletePuppyTest(TestCase):
    """Test for deleting puppy"""
    def setUp(self):
        self.kaliya = Puppy.objects.create(
            name = 'Kaliya', age = 5, breed = 'Stray', color = 'Black'
        )
        self.wadi = Puppy.objects.create(
            name = 'Wadi', age = 2, breed = 'Stray', color = 'Brown'
        )

    def test_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_puppy', kwargs={'pk':self.kaliya.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_puppy', kwargs={'pk':30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)