from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': 'O que está acontecendo?',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escreva sua postagem...',
                'maxlength': 280,
            })
        }
