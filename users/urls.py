from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from . import views
from users.forms import EmailValidationOnForgotPassword

app_name = "users"

urlpatterns = [
    path("registeruser/", views.RegisterUserView.as_view(), name="register_user"),
    path(
        "registerrestaurant/",
        views.RegisterRestaurantView.as_view(),
        name="register_restaurant",
    ),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myaccount/", views.my_account, name="my_account"),
    path("customer-dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path(
        "restaurant-dashboard/", views.restaurant_dashboard, name="restaurant_dashboard"
    ),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path('reset-password/', PasswordResetView.as_view(
        template_name="users/passwordreset/password_reset_form.html",
        email_template_name="users/passwordreset/password_reset_email.html",
        success_url=reverse_lazy('users:password_reset_done'),
        form_class=EmailValidationOnForgotPassword
    ),
         name='reset_password'),
    path('password-reset-done/',
         PasswordResetDoneView.as_view(template_name="users/passwordreset/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="users/passwordreset/password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete")),
         name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name="users/passwordreset/password_reset_complete.html",
    ), name='password_reset_complete'),
]
