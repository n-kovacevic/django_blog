from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Tag(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    content = MarkdownxField()
    author = models.ForeignKey(User, models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    tags = models.ManyToManyField(Tag)

    @property
    def markdown_content(self):
        return markdownify(self.content)

    class Meta:
        ordering = ['-date_created']


