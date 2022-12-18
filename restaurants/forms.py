from django import forms

from users.validators import image_validator

from .models import Restaurant


class RestaurantRegistrationForm(forms.ModelForm):
    license = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[image_validator],
    )

    class Meta:
        model = Restaurant
        fields = ["name", "license"]
