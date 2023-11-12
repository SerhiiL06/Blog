from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(
        max_length=20,
        help_text="Enter you city",
        label="City",
    )
