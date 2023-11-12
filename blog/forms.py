from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    tag = forms.ModelChoiceField(Tag.objects.all())

    class Meta:
        model = Post
        fields = ["title", "text", "image", "category", "tag"]


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text"]


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter your comment here"})
    )

    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Your comment"}


class SearchForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Post
        exclude = ["post", "author"]
