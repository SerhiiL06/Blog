from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r"posts", views.PostViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"users", views.UserViewSet)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("weather/", views.WeatherView.as_view(), name="weather"),
]


urlpatterns += router.urls
