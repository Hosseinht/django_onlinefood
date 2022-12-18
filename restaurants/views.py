from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from profiles.forms import ProfileForm
from profiles.models import Profile

from .forms import RestaurantRegistrationForm
from .models import Restaurant


def check_role_restaurant(user):
    # restrict restaurant from accessing to the customer page
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


@login_required(login_url="users:login")
@user_passes_test(check_role_restaurant)
def restaurant_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    restaurant = get_object_or_404(Restaurant, user=request.user)

    if request.method == "POST":
        restaurant_form = RestaurantRegistrationForm(
            request.POST, request.FILES, instance=restaurant
        )
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
    return render(request, "restaurant/restaurant_profile.html", context)


def menu_builder(request):
    return render(request, 'restaurant/menu_builder.html')
