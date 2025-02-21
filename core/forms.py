from django import forms
from django.core.exceptions import ValidationError

from .models import PostCategory, Post


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')


class PostAddModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['profile']


class PostAddForm(forms.Form):
    title = forms.CharField(label='Заголовок')
    text = forms.CharField(label='Текст', widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=PostCategory.objects.all(),
                                      label='Категория'
                                      )

    def clean_text(self):
        text = self.cleaned_data['text']
        words = ['дурак', 'козел']
        for word in words:
            if word in text:
                raise ValidationError('В тексте есть запрещенные слова ⚠')
        return text


class FeedbackForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class CommentAddForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 15:
            raise ValidationError('Длина должна быть не больше 15')
        return title


class PostFilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(
        queryset=PostCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории',
        required=False)
    order = forms.ChoiceField(
        choices=[('like_desc', 'много лайков'), ('like_asc', 'мало лайков'), ('new', 'новые'),  ('old', 'старые')],
        label='Сортировка',
        required=False)
