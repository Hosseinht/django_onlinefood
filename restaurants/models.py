from django.conf import settings
from django.contrib import admin
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL


def get_restaurant_license_path(restaurant, filename):
    return "restaurants/license/%s/%s" % (str(restaurant.name), filename)


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    license = models.ImageField(upload_to=get_restaurant_license_path)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @admin.display(ordering='user__first_name')
    def user_name(self):
        return self.user.get_full_name
