from django.contrib import admin

from .models import Post, Feedback, PostCategory, PostComment

admin.site.register(Post)
admin.site.register(Feedback)
admin.site.register(PostCategory)
admin.site.register(PostComment)
