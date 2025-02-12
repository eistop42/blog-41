from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='profiles_home'),
    path('login', views.login, name='profiles_login'),
    path('register', views.register, name='profiles_register'),
    path('logout', views.logout, name='profiles_logout')
]
