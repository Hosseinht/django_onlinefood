from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RestaurantRegistrationForm
from .models import Restaurant
from profiles.models import Profile
from profiles.forms import ProfileForm


def restaurant_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    restaurant = get_object_or_404(Restaurant, user=request.user)

    if request.method == "POST":
        restaurant_form = RestaurantRegistrationForm(request.POST, request.FILES, instance=restaurant)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if restaurant_form.is_valid() and profile_form.is_valid():
            restaurant_form.save()
            profile_form.save()
            messages.success(request, "Settings updated")
            return redirect("users:restaurant_profile")
    else:
        restaurant_form = RestaurantRegistrationForm(instance=restaurant)
        profile_form = ProfileForm(instance=profile)

    context = {
        "restaurant_form": restaurant_form,
        "profile_form": profile_form,
        "profile": profile,
        "restaurant": restaurant,
    }
    return render(request, 'restaurant/restaurant_profile.html', context)
