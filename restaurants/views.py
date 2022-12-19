from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from profiles.forms import ProfileForm
from profiles.models import Profile

from .forms import RestaurantRegistrationForm, CategoryForm
from .models import Category, FoodItem, Restaurant


def get_restaurant(request):
    restaurant = Restaurant.objects.get(user=request.user)
    return restaurant


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


@login_required(login_url="users:login")
@user_passes_test(check_role_restaurant)
def menu_builder(request):
    restaurant = get_restaurant(request)
    category = Category.objects.filter(restaurant=restaurant).order_by('created_at')

    context = {"restaurant": restaurant, "category": category}

    return render(request, "restaurant/menu_builder.html", context)


@login_required(login_url="users:login")
@user_passes_test(check_role_restaurant)
def category_fooditems(request, pk):
    restaurant = get_restaurant(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(category=category, restaurant=restaurant)

    context = {"fooditems": fooditems, "category": category}
    return render(request, "restaurant/category_fooditems.html", context)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.save(commit=False)
            category.restaurant = get_restaurant(request)
            category.slug = slugify(name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('users:menu_builder')
    else:
        form = CategoryForm()

    context = {
        "form": form
    }

    return render(request, "restaurant/add_category.html", context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.save(commit=False)
            category.restaurant = get_restaurant(request)
            category.slug = slugify(name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('users:menu_builder')
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
    }
    return render(request, 'restaurant/edit_category.html', context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('users:menu_builder')


def add_fooditem(request, pk=None):
    category = get_object_or_404(Category, pk=pk)

    return render(request, 'restaurant/add_fooditem.html')
