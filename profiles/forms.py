from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "cover_photo",
            "address_line_1",
            "address_line_2",
            "country",
            "state",
            "city",
            "postal_code",
            "latitude",
            "longitude",
        ]
