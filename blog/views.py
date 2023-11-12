from datetime import datetime


from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from weather.apiweather import get_weather


from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .forms import CommentForm, PostForm, SearchForm, UpdatePostForm
from .models import Category, Comment, FavoriteList, Post


class IndexView(TitleMixin, TemplateView):
    title = "My blog"
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Post.objects.filter(published=True).values(
            "slug", "title", "text"
        )[:3]
        context["time"] = datetime.now()
        context["weather"] = get_weather()
        return context


# List, Detail post
class PostsView(TitleMixin, ListView):
    title = "All posts"
    template_name = "blog/posts.html"
    queryset = Post.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        if self.kwargs.get("tag_id"):
            context["user_post"] = Post.objects.filter(
                author=self.request.user
            ).distinct()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        category_id = self.kwargs.get("category_id")
        tag = self.kwargs.get("tag_id")
        return (
            queryset.filter(Q(category_id=category_id) | Q(tag=tag))
            if category_id or tag
            else queryset
        )


class DetailPostView(TitleMixin, View):
    title = "Detail"

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        form = CommentForm()
        session = request.session.get("key", [])

        if not session:
            session = request.session["key"] = []
        if post.slug not in session:
            session.append(post.slug)

        post.views += 1
        post.save()
        context = {
            "object": post,
            "title": "Detail",
            "comment_form": form,
            "comments": post.comments.all().order_by("-created_date"),
        }
        return render(request, "blog/post-detail.html", context=context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            post = Post.objects.get(slug=slug)
            Comment.objects.create(author=self.request.user, text=text, post=post)
            messages.success(request, "Good work!")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


def delete_comment(request, id):
    comment = Comment.objects.filter(id=id, author=request.user)
    if comment.first():
        comment.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


# Creating, Update, Delete
class CreatePostView(TitleMixin, CreateView):
    title = "Create post"
    model = Post
    template_name = "blog/create-post.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class UpdatePostView(TitleMixin, UpdateView):
    title = "Update post"
    template_name = "blog/update.html"
    model = Post
    form_class = UpdatePostForm
    success_url = reverse_lazy("blog:my-posts")

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        if str(post.author) != self.request.user.username:
            raise PermissionDenied("Доступ запрещен")

        return post

    def post(self, request, pk):
        post = self.get_object()
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def remove_post(request, post_id):
    post_to_remove = Post.objects.get(id=post_id)
    post_to_remove.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class PostUserList(TitleMixin, ListView):
    title = "Post list"
    template_name = "blog/list_user.html"
    model = Post

    def total_posts(self):
        all = Post.objects.filter(author=self.request.user)
        return len(all)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["total_posts"] = self.total_posts()
        return context


def search_request(request):
    if request.method == "GET":
        form = SearchForm()
        return render(request, "blog/search.html", {"form": form})
    if request.method == "POST":
        result = request.POST.get("search_query")
        posts = Post.objects.filter(
            Q(text__icontains=result) | Q(title__icontains=result)
        )
        return render(request, "blog/search.html", {"posts": posts})


# Favorite list and add to this list
class FavoriteListView(ListView):
    model = FavoriteList
    template_name = "blog/favorite_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        queryset.filter(user=user)
        return queryset.filter(user=user)


@login_required()
def add_or_delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    favlist = FavoriteList.objects.filter(user=user, post=post)
    if not favlist.exists():
        FavoriteList.objects.create(user=user, post=post)
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        favlist.delete()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
