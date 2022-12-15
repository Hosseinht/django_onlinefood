from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from restaurants.forms import RestaurantRegistrationForm
from restaurants.models import Restaurant

from .forms import UserRegistrationForm
from .models import User
from .token import user_activation_token
from .utils import detect_user, send_verification_email


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
    success_url = reverse_lazy("users:register_user")

    def dispatch(self, request, *args, **kwargs):
        """
        Authenticated users shouldn't see the User registration page
        """
        if request.user.is_authenticated:
            return redirect("users:my_account")
        return super(RegisterUserView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data["password"]

        user = form.save(commit=False)
        user.set_password(password)
        user.role = User.CUSTOMER
        user.save()

        # send verification email to the users
        send_verification_email(self.request, user)

        messages.success(
            self.request,
            "Please confirm your email address to complete the registration",
        )
        return super(RegisterUserView, self).form_valid(form)


class RegisterRestaurantView(generic.CreateView):
    template_name = "users/register_restaurant.html"
    form_class = UserRegistrationForm
    second_form_class = RestaurantRegistrationForm

    def get_success_url(self):
        return reverse("users:register_restaurant")

    def dispatch(self, request, *args, **kwargs):
        """
        Authenticated users shouldn't see the Restaurant registration page
        """
        if request.user.is_authenticated:
            return redirect("users:dashboard")
        return super(RegisterRestaurantView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegisterRestaurantView, self).get_context_data(**kwargs)
        if "user_form" not in context:
            context["user_form"] = self.form_class()
        if "restaurant_form" not in context:
            context["restaurant_form"] = self.second_form_class()
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

            # send verification email to the users
            send_verification_email(self.request, user)

            messages.success(
                request,
                "Please confirm your email address to complete the registration.",
            )
            return super(RegisterRestaurantView, self).post(
                self, request, *args, **kwargs
            )


def activate(request, uidb64, token):
    # Activate the users by setting the is_active status to True

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user_activation_token.check_token(user, token):

        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("users:my_account")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("users:my_account")


def login(request):
    if request.user.is_authenticated:
        return redirect("users:my_account")
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You were successfully logged in.")
            return redirect("users:my_account")
        else:
            messages.error(request, "Invalid login credential")
            return redirect("users:login")

    return render(request, "users/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect("users:login")


@login_required(login_url="users:login")
def my_account(request):
    """
    Redirect users based on the users role
    """
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


@login_required(login_url="users:login")
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    """
    my_account function check the users and if the users was a customer, will be redirected here
    """
    return render(request, "users/customer_dashboard.html")


@login_required(login_url="users:login")
@user_passes_test(check_role_restaurant)
def restaurant_dashboard(request):
    """
    my_account function check the users and if the users was a restaurant, will be redirected here
    """
    restaurant = Restaurant.objects.get(user=request.user)
    context = {
        'restaurant': restaurant
    }
    return render(request, "users/restaurant_dashboard.html", context)
