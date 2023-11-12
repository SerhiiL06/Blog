from django.contrib.auth.decorators import login_required
from django.urls import path


from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts/", views.PostsView.as_view(), name="posts"),
    path(
        "posts/category/<int:category_id>/", views.PostsView.as_view(), name="category"
    ),
    path("posts/tag/<int:tag_id>/", views.PostsView.as_view(), name="tag-posts"),
    path(
        "post/<slug:slug>/",
        login_required(views.DetailPostView.as_view()),
        name="detail",
    ),
    path(
        "post/add-comment/<slug:slug>/",
        login_required(views.DetailPostView.as_view()),
        name="comment",
    ),
    path(
        "post/delete_comment/<int:id>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "posts/my-posts/", login_required(views.PostUserList.as_view()), name="my-posts"
    ),
    path("post/delete/<int:post_id>/", views.remove_post, name="remove_post"),
    path("post/update/<int:pk>/", views.UpdatePostView.as_view(), name="update"),
    path(
        "favorite_list/",
        login_required(views.FavoriteListView.as_view()),
        name="favorite_list",
    ),
    path("posts/adddelfav/<int:post_id>/", views.add_or_delete_post, name="favorite"),
    path(
        "posts/create/", login_required(views.CreatePostView.as_view()), name="create"
    ),
    path("search/", views.search_request, name="search"),
]
