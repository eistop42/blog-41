from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='profiles_home'),
    path('login', views.login, name='profiles_login'),
]
