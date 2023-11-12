from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class Address(models.Model):
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField(validators=[MaxValueValidator(9999)])

    def __str__(self) -> str:
        return self.city

    class Meta:
        verbose_name_plural = "Address"


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    image = models.ImageField(upload_to="users_image/", blank=True)
    is_verification = models.BooleanField(default=False)
    address = models.OneToOneField(
        to=Address, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    validity_period = models.DateTimeField()

    def sending(self):
        link = f"http://127.0.0.1:8000/users/emailverif/{self.user.email}/{self.code}/"
        subject = f"Verification for {self.user.first_name}"
        message = f"For your verification click here {link}"
        mail = "example@gmail.com"
        to = [self.user.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=mail,
            recipient_list=to,
            fail_silently=False,
        )

    def is_validity(self):
        return self.validity_period >= timezone.now()

    def __str__(self):
        return f"Email for {self.user.username}"
