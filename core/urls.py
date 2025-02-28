from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/like', views.post_like, name='post_like'),
    path('posts/<int:post_id>/unlike', views.post_unlike, name='post_unlike'),

    path('posts/<int:post_id>/comments/<comment_id>/delete', views.comment_delete, name='comment_delete'),
    path('posts/add', views.post_add, name='post_add'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback/success', views.feedback_success, name='feedback_success'),

    path('vue', views.vue, name='vue'),


    # path('posts/<int:post_id>/comments', views.comment_add, name='comment_add')
]
