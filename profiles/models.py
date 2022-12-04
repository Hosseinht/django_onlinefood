from django.conf import settings
from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models


def get_profile_picture_path(profile, filename):
    return "users/profile_picture/%s/%s" % (str(profile.user.username), filename)


def get_cover_photo_path(profile, filename):
    return "users/cover_photo/%s/%s" % (str(profile.user.username), filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=get_profile_picture_path, blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to=get_cover_photo_path, blank=True, null=True
    )
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^(\+\d{1,3})?,?\s?\d{8,13}",
        message="Phone number must not consist of space and requires country code. eg : +6591258565",
    )
    phone_number = models.CharField(
        max_length=13, validators=[phone_regex], null=True, blank=True
    )
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    @admin.display()
    def email(self):
        return self.user.email

    @admin.display()
    def full_name(self):
        return self.user.get_full_name
