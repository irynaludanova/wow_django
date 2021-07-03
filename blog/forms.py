from django import forms
from django.forms import ModelForm
from .models import Comment, Post
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'image', 'category', 'title', 'text', 'url']


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }

