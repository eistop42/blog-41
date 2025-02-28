from django.db import models

from profiles.models import Profile


class PostCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(max_length=255, verbose_name='Текст')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL,
                                 verbose_name='Категория')
    image = models.ImageField(upload_to='images', verbose_name='Картинка', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_posts', blank=True, null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_date']

    def __str__(self):
        return self.title


class PostComment(models.Model):
    title = models.CharField(max_length=500, verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_comments',
                                blank=True, null=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']

    def __str__(self):
        return self.title


class Feedback(models.Model):
    text = models.TextField(max_length=255, verbose_name='Текст')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_date']

    def __str__(self):
        return self.text


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_likes')
    is_liked = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.post}-{self.profile}'
