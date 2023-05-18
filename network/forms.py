from django import forms
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

        labels = {
            'body':'',
        }

        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'autocomplete': 'off', 'rows':2, 'id':'post-form',}),
        }