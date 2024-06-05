from django.db import models
from django.conf import settings
from reviews.models import Reivew

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    review = models.ForeignKey(Reivew, on_delete = models.CASCADE)