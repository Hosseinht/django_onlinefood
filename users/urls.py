from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("registeruser/", views.register_user, name="register_user"),
]
