from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),

    path('posts/add', views.post_add, name='post_add'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback/success', views.feedback_success, name='feedback_success'),

    # path('posts/<int:post_id>/comments', views.comment_add, name='comment_add')
]
