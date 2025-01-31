from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.layout import Submit



from .models import PostCategory

class PostAddForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=PostCategory.objects.all())



    def clean_title(self):
        title = self.cleaned_data['title']
        if title == 'привет':
            raise ValidationError('Недопустимый заголовок')
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'post-add'
        self.helper.form_method = 'post'
        self.helper.form_action = 'post_add'
        self.helper.add_input(Submit('submit', 'Добавить'))