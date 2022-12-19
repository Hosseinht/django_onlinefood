from django.urls import include, path, reverse_lazy

from users.views import restaurant_dashboard

from . import views

# app_name = "restaurants"

urlpatterns = [
    path("", restaurant_dashboard),
    path("profile/", views.restaurant_profile, name="restaurant_profile"),
    path("menu-builder/", views.menu_builder, name="menu_builder"),

    # Category
    path(
        "menu-builder/category/<int:pk>/",
        views.category_fooditems,
        name="category_fooditems",
    ),
    path(
        "menu-builder/category/<int:pk>/edit/",
        views.edit_category,
        name="edit_category",
    ),
    path(
        "menu-builder/category/<int:pk>/delete/",
        views.delete_category,
        name="delete_category",
    ),
    path("menu-builder/category/add/", views.add_category, name="add_category"),

    # FoodItems
    path(
        "menu-builder/category/<int:pk>/add-fooditem/",
        views.add_fooditem,
        name="add_fooditem.html",
    ),
]
