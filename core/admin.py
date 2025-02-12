from django.contrib import admin

from .models import Post, Feedback, PostCategory, PostComment, PostLike

admin.site.register(Post)
admin.site.register(Feedback)
admin.site.register(PostCategory)
admin.site.register(PostComment)
admin.site.register(PostLike)
