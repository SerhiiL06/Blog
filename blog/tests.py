from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class IndexViewTest(TestCase):
    def test_index(self):
        path = reverse("blog:index")
        responce = self.client.get(path)

        self.assertTemplateUsed(responce, "blog/index.html")


class UserPostsViewTest(TestCase):
    def test_page(self):
        path = reverse("blog:my-posts")
        responce = self.client.get(path)

        self.assertAlmostEqual(responce.status_code, HTTPStatus.OK)
