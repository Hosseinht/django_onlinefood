from django.urls import path, reverse_lazy, include

from . import views
from users.views import restaurant_dashboard

# app_name = "restaurants"

urlpatterns = [

    path('', restaurant_dashboard),
    path('profile/', views.restaurant_profile, name='restaurant_profile')
]
