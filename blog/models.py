from django.db.models.query import QuerySet
from .validators import max_len_validator
from django.db import models
from users.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Tag(models.Model):
    caption = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.caption


class PostManager(models.Manager):
    def published(self):
        return super().get_queryset().filter(published=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(validators=[max_len_validator])
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(editable=False)
    published = models.BooleanField(default=True)
    slug = models.SlugField(default="", blank=True, null=False)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    tag = models.ManyToManyField(to=Tag, related_name="posts")

    objects = PostManager()

    def __str__(self):
        return f"Post from {self.author} about {self.title} ({self.created.date()})"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def in_list(self):
        post = FavoriteList.objects.filter(user=self.author, post=self)
        return post.exists()

    def len_text(self):
        return len(self.text) > 50

    class Meta:
        ordering = ["-created"]


class Comment(models.Model):
    text = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self) -> str:
        return f"Comment from {self.author.username}"


class FavoriteList(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
