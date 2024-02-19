from django import forms
from .models import Post, Response
class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['title','text','price', 'category']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
