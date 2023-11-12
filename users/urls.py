from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "emailverif/<str:email>/<uuid:code>/",
        views.EmailverificationView.as_view(),
        name="verif",
    ),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("block-time/", views.DefenderBlockView.as_view(), name="defender"),
]
