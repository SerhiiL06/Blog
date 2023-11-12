from typing import Any
from django.contrib.auth.views import LoginView

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from common.views import TitleMixin

from .forms import LoginForm, RegisterForm, UpdateUserForm
from .models import EmailVerification, User


class RegisterView(TitleMixin, CreateView):
    title = "Register"
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")

    def save(self, *args, **kwargs):
        my_session = self.request.session.get("username")
        self.request.session["test"] = my_session
        super().save(*args, **kwargs)


class LoginUserView(TitleMixin, LoginView):
    title = "Login page"
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("blog:index")


@method_decorator(login_required, name="dispatch")
class ProfileView(UpdateView):
    template_name = "users/profile.html"
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        if self.request.user.id != self.kwargs.get("pk"):
            raise PermissionDenied("Wrong!")

        return self.request.user

    def post(self, request, pk):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = self.request.user
            user.address = form.cleaned_data["address"]
            form.save()
        return render(request,"users/profile.html", {"form": form})


class EmailverificationView(TemplateView):
    template_name = "users/email.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verification = EmailVerification.objects.filter(code=code, user=user)
        if email_verification.exists() and email_verification.first().is_validity():
            user.is_verification = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return reverse("blog:index")


class DefenderBlockView(TemplateView):
    template_name = "users/defender.html"
