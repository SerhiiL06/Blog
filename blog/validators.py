from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator


def max_len_validator(value):
    if len(value) > 1000:
        raise ValidationError(f"Sorry {value} is not supports")
