from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class RegisterViewTestCase(TestCase):
    def test_register(self):
        path = reverse("users:register")
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
