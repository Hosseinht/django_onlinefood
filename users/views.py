from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .forms import UserRegistrationForm
from .models import User
from .utils import detect_user

from restaurants.forms import RestaurantRegistrationForm


# restrict restaurant from accessing to the customer page
def check_role_restaurant(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# restrict customer from accessing to the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


class RegisterUserView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = "users/register_user.html"

    def get_success_url(self):
        return reverse("users:register_user")

    def dispatch(self, request, *args, **kwargs):
        """
           Authenticated user shouldn't see the User registration page
        """
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        return super(RegisterUserView, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        """
            Authenticated user shouldn't see the Restaurant registration page
        """
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        return super(RegisterRestaurantView, self).dispatch(request, *args, **kwargs)

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


def login(request):
    if request.user.is_authenticated:
        return redirect('users:my_account')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('users:my_account')
        else:
            messages.error(request, "Invalid login credential")
            return redirect('users:login')

    return render(request, 'users/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('users:login')


@login_required(login_url='users:login')
def my_account(request):
    """
        Redirect user based on the user role
    """
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


@login_required(login_url='users:login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'users/customer_dashboard.html')


@login_required(login_url='users:login')
@user_passes_test(check_role_restaurant)
def restaurant_dashboard(request):
    return render(request, 'users/restaurant_dashboard.html')


