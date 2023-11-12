import uuid
from datetime import timedelta
from django import forms
from .models import User, EmailVerification, Address
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "enter your username"})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "enter your name"})
    )
    last_name = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "first_name",
            "last_name",
        ]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=True)
        period = timezone.now() + timedelta(hours=72)
        record = EmailVerification.objects.create(
            user=user, code=uuid.uuid4(), validity_period=period
        )
        record.sending()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password"]


class UpdateUserForm(forms.ModelForm):
    address = forms.ModelChoiceField(Address.objects.all())

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
