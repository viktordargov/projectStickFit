from django import forms
from .models import ForumThreads, Comment


class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThreads
        fields = ['title', 'content',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
