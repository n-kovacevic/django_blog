from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Post, Tag


class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ['author']

    tags = ModelMultipleChoiceField(queryset=Tag.objects)
