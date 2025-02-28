from django.urls import path

from . import views

urlpatterns = [
    path('main', views.main, name='api_main'),
    path('posts', views.posts, name='api_posts'),
]
