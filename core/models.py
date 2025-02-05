from django.db import models



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
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Категория')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_date']

    def __str__(self):
        return self.title


class PostComment(models.Model):
    title = models.CharField(max_length=500, verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

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