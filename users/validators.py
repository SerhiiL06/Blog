from django.core.exceptions import ValidationError


def max_value(value):
    if int(value) > 9999:
        raise ValidationError("Sorry, your code have problem")
