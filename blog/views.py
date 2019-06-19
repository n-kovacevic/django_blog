from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.static import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect

from .models import Comment, Post, Tag
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
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()
        return redirect(reverse_lazy('blog:post_view', kwargs={'pk': post.pk}))

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


class CommentMixin:
    model = Comment


class CommentFormMixin(LoginRequiredMixin, CommentMixin):
    request = None
    fields = ['content']
    kwargs = {}

    def form_valid(self, form):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise Http404()


class ReplyCommentFormMixin(CommentFormMixin):

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.parent = get_object_or_404(Comment, pk=self.kwargs['pk'])
        comment.save()
        return redirect(reverse_lazy('blog:post_view', kwargs={'pk': self.kwargs['post_pk']}))


class PostCommentFormMixin(CommentFormMixin):

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        comment.save()
        return redirect(reverse_lazy('blog:post_view', kwargs={'pk': self.kwargs['post_pk']}))


class NewCommentView(PostCommentFormMixin, CreateView):
    pass


class NewCommentReplyView(ReplyCommentFormMixin, CreateView):
    pass


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, CommentMixin, DeleteView):

    @property
    def success_url(self):
        return reverse_lazy('blog:post_view', kwargs={'pk': self.kwargs['post_pk']})

    def test_func(self):
        return self.get_object().author == self.request.user
