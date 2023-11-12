from blog.serializers import PostSerializer, CategorySerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from django.views.generic import View
from django.shortcuts import render
from .forms import WeatherForm
from weather.apiweather import get_weather
from django.contrib import messages

from blog.models import Post, Category
from users.serializers import UserSerializer
from users.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["views"]
    search_fields = ["title"]
    ordering_fields = ["views"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WeatherView(View):
    def get(self, request):
        form = WeatherForm()
        return render(request, "api/weather.html", {"form": form})

    def post(self, request):
        form = WeatherForm(request.POST)
        city = request.POST.get("city")
        try:
            weather = get_weather(city=city)
            context = {"form": form, "weather": weather, "city": city}
            return render(request, "api/weather.html", context)
        except:
            messages.error(request, "Enter correct city")
            return render(request, "api/weather.html", {"form": form})
