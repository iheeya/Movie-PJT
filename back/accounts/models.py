from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie


# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    likes = models.ManyToManyField(Movie, symmetrical=False)