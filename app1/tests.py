from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from app1.api import serializers
from app1 import models


class StreamingPlatformTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="ex", password="qw@123")
        self.token = Token.objects.get(user__username = "ex")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamingPlatform.objects.create(name="Netflix", 
                                about="#1 Platform", website="https://www.netflix.com")
        
    def test_create(self):
        data = {
            "name" : "Netflix",
            "about" : "#1 Platform",
            "website" : "https://www.netflix.com"
        }
        response = self.client.post(reverse('platform'), data)
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        
    def test_list(self):
        response = self.client.get(reverse('platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_details(self):
        response = self.client.get(reverse('platform_detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class WatchTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="ex", password="qw@123")
        self.token = Token.objects.get(user__username = "ex")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamingPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
        self.watch = models.Watch.objects.create(title = "ex1", description = "example one", active = True, platform = self.stream)
        
    def test_create(self):
        data = {
            "title" : "ex1",
            "description" : "example one",
            "active" : True,
            "platform" : self.stream
        }
        response = self.client.post(reverse('list'), data)
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        
    def test_list(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_details(self):
        response = self.client.get(reverse('list_detail', args=(self.watch.id, )))    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Watch.objects.count(), 1)
        self.assertEqual(models.Watch.objects.get().title, "ex1")
        
    class ReviewTest(APITestCase):
        
        def setUp(self):
            self.user = User.objects.create_user(username="ex", password="qw@123")
            self.token = Token.objects.get(user__username = "ex")
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            self.stream = models.StreamingPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
            self.watch = models.Watch.objects.create(title = "ex1", description = "example one", active = True, platform = self.stream)
            self.review = models.Review.objects.create(user= self.user, ratings = 5, reviews = "great movie", watchlist = self.watch, active = True)
            
        def test_create(self):
            data = {
            "user": self.user,
            "ratings": 5,
            "reviews": "greate movie",
            "watchlist": self.watch,
            "active": True
            }
            
            response = self.client.post(reverse('Create_review', args=(self.watch.id)), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
        def test_update(self):
            data = {
            "user": self.user,
            "ratings": 5,
            "reviews": "greate movie - update",
            "watchlist": self.watch,
            "active": True
            }
            
            response = self.client.post(reverse('review_details', args=(self.watch.id)), data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
        def test_details(self):
            response = self.client.get(reverse('review_details', args=(self.watch.id)))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
        def test_delete(self):
            response = self.client.delete(reverse('review_details', args=(self.watch.id)))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_user(self):
            response = self.client.get('/watch/user/?username=' + self.user.username)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        