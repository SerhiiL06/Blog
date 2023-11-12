from django.contrib import admin
from .models import Category, Post, FavoriteList, Tag, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "views", "published", "author"]
    fields = ["title", "text", "slug", "tag", "views", "published"]
    list_filter = ["published"]
    prepopulated_fields = {
        "slug": ["title"],
    }
    filter_horizontal = ["tag"]
    actions = ["set_published"]

    @admin.action(description="Edit pub")
    def set_published(self, request, queryset):
        username = ["Milana"]
        queryset.filter(author__username__in=username).update(published=False)
        return queryset


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ["user"]
