from typing import Dict, Any, Union

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Tag, Comment
from .forms import PostForm


class PostMixin:
    model = Post


class PostListView(PostMixin, ListView):
    paginate_by = 5


class PostDetailView(PostMixin, DetailView):
    pass


class PostFormMixin(LoginRequiredMixin, PostMixin):
    request = None
    form_class = PostForm

    def form_valid(self, form):
        object_ = form.save(commit=False)
        object_.author = self.request.user
        object_.save()
        form.save_m2m()
        return redirect(reverse_lazy('blog:post_view', kwargs={'pk': object_.pk}))

    def post(self, request, *args, **kwargs):
        post_tags = request.POST.getlist('tags')
        for tag_name in post_tags:
            if not Tag.objects.filter(name=tag_name):
                Tag.objects.create(name=tag_name)
        return super().post(request, *args, **kwargs)


class NewPostView(PostFormMixin, CreateView):
    pass


class EditPostView(PostFormMixin, UpdateView):
    pass


class DeletePostView(LoginRequiredMixin, PostMixin, DeleteView):
    success_url = reverse_lazy('blog:home')


class TagPostListView(PostListView):
    TAG_ARG = 'tag'

    def get(self, request, *args, **kwargs):
        if self.TAG_ARG in kwargs:
            self.tag_name = kwargs[self.TAG_ARG]
        return super().get(request, args, kwargs)

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.tag_name) if self.tag_name else super().get_queryset()

    @property
    def tag_name(self):
        tag_name = None
        try:
            tag_name = self.extra_context[self.TAG_ARG]
        except KeyError:
            pass
        return tag_name

    @tag_name.setter
    def tag_name(self, value):
        self.extra_context = self.extra_context if self.extra_context else dict()
        self.extra_context[self.TAG_ARG] = value


class ExtraGetParametersMixin:
    extra_context: Union[Dict[Any, Any], Any]
    GET_PARAMS = 'get_params'
    excluded_params = ['page', ]

    def get(self, request, *args, **kwargs):
        self.extra_context = self.extra_context if self.extra_context else dict()
        self.extra_context[self.GET_PARAMS] = {
            k: v for k, v in dict(request.GET).items() if k not in self.excluded_params}
        return super().get(request, args, kwargs)


class SearchPostListView(PostListView):

    SEARCH_ARG = 'q'

    def get(self, request, *args, **kwargs):
        if self.SEARCH_ARG in request.GET:
            self.search_query = request.GET[self.SEARCH_ARG]
        return super().get(request, args, kwargs)

    @property
    def search_query(self):
        query = None
        try:
            query = self.extra_context[self.SEARCH_ARG]
        except KeyError:
            pass
        return query

    @search_query.setter
    def search_query(self, value):
        self.extra_context = self.extra_context if self.extra_context else dict()
        self.extra_context[self.SEARCH_ARG] = value

    def get_queryset(self):
        return Post.objects.filter(Q(title__contains=self.search_query) | Q(summary__contains=self.search_query))


def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    author = request.user
    content = request.POST['comment']
    comment = Comment(author=author, content=content, post=post)
    comment.save()
    post.comment_set.add(comment)
    return redirect('blog:post_view', pk=post_pk)


def comment_reply(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    author = request.user
    content = request.POST['content']
    reply = Comment(author=author, content=content, parent=comment)
    reply.save()
    return redirect('blog:post_view', pk=post_pk)