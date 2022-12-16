from django import forms

from .models import Restaurant


class RestaurantRegistrationForm(forms.ModelForm):
    license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Restaurant
        fields = ['name', 'license']
