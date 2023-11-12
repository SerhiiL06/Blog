from rest_framework import serializers
from .models import Post, Category
from django.utils.text import slugify
from django.utils import timezone


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    category = serializers.ReadOnlyField(source="category.title")
    views = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ["id", "title", "text", "author", "category", "views"]


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=250)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.save()
        return instance
