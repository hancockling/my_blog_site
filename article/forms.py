from django import forms
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag
from django.forms import TextInput


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ['column']


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ['title', 'body']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ['tag']

        widgets = {
            'tag': TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
