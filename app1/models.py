from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField(max_length=255)
    website = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Watch(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(
        StreamingPlatform, on_delete=models.CASCADE, related_name="watchlist"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category"
    )
    trailer = models.URLField(null=True, blank=True)
    avg_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    reviews = models.CharField(max_length=255)
    watchlist = models.ForeignKey(
        Watch, on_delete=models.CASCADE, related_name="Show_reviews"
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | {self.ratings} | {self.watchlist.title}"
