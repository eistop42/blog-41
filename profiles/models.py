from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()


class ProfileSubscription(models.Model):
    profile = models.ForeignKey(Profile, related_name='subscriptions', on_delete=models.CASCADE)
    author =   models.ForeignKey(Profile, related_name='subscribers', on_delete=models.CASCADE)