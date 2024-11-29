from django import forms
from .models import ForumPost, Comment


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
