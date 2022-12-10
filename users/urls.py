from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("registeruser/", views.RegisterUserView.as_view(), name="register_user"),
    path("registerrestaurant/", views.register_restaurant, name="register_restaurant"),
]
