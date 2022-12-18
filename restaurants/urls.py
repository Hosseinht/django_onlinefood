from django.urls import include, path, reverse_lazy

from users.views import restaurant_dashboard

from . import views

# app_name = "restaurants"

urlpatterns = [
    path("", restaurant_dashboard),
    path("profile/", views.restaurant_profile, name="restaurant_profile"),
    path("menu-builder/", views.menu_builder, name="menu_builder"),
]
