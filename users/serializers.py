from rest_framework import serializers
from .models import User
from blog.serializers import PostSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "posts"]
