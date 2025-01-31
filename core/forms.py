from django import forms
from .models import PostCategory

class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')


class PostAddForm(forms.Form):
    title = forms.CharField(label='Заголовок')
    text = forms.CharField(label='Текст', widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=PostCategory.objects.all(),
                                      label='Категория'
                                      )

class FeedbackForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)