from django.contrib import admin

from .models import Profile, ProfileSubscription

admin.site.register(Profile)
admin.site.register(ProfileSubscription)
