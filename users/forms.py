from django import forms

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    def clean(self):
        data = super(UserRegistrationForm, self).clean()
        password = data["password"]
        confirm_password = data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
