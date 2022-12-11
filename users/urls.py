from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("registeruser/", views.RegisterUserView.as_view(), name="register_user"),
    path("registerrestaurant/", views.RegisterRestaurantView.as_view(), name="register_restaurant"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myaccount/", views.my_account, name="my_account"),
    path("customerdashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("restaurantdashboard/", views.restaurant_dashboard, name="restaurant_dashboard"),

]
