from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .forms import UserRegistrationForm
from .models import User

from restaurants.forms import RestaurantRegistrationForm


class RegisterUserView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = "users/register_user.html"

    def get_success_url(self):
        return reverse("users:register_user")

    def form_valid(self, form):
        password = form.cleaned_data["password"]

        user = form.save(commit=False)
        user.set_password(password)
        user.role = User.CUSTOMER
        user.save()
        messages.success(self.request, "Your account has been created successfully")
        return super(RegisterUserView, self).form_valid(form)


class RegisterRestaurantView(generic.CreateView):
    template_name = "users/register_restaurant.html"
    form_class = UserRegistrationForm
    second_form_class = RestaurantRegistrationForm

    def get_success_url(self):
        return reverse("users:register_restaurant")

    def get_context_data(self, **kwargs):
        context = super(RegisterRestaurantView, self).get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = self.form_class()
        if 'restaurant_form' not in context:
            context['restaurant_form'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        restaurant_form = RestaurantRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            password = user_form.cleaned_data["password"]

            user = user_form.save(commit=False)
            user.set_password(password)
            user.role = User.RESTAURANT
            user.save()

            restaurant = restaurant_form.save(commit=False)
            restaurant.user = user
            restaurant.save()
            messages.success(request, "Your account has been created successfully. Please wait for approval")
            return super(RegisterRestaurantView, self).post(self, request, *args, **kwargs)
