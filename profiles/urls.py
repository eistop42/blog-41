from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='profiles_home'),
    path('<int:profile_id>/subscribe', views.profile_subscribe, name='subscribe'),
    path('login', views.login, name='profiles_login'),
    path('register', views.register, name='profiles_register'),
    path('logout', views.logout, name='profiles_logout')
]
