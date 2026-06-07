from django import forms

from .models import Comment, Post


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comentário',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Escreva um comentário...',
                'maxlength': 280,
            })
        }
