from django import forms

from users.validators import image_validator

from .models import Profile


class ProfileForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type your address...",
                "required": "required",
                "class": "text-muted",
            }
        )
    )
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[image_validator],
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[image_validator],
    )
    latitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "postal_code",
            "latitude",
            "longitude",
        ]
