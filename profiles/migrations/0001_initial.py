# Generated by Django 4.1.3 on 2022-12-03 15:36

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import profiles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=profiles.models.get_profile_picture_path,
                    ),
                ),
                (
                    "cover_photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=profiles.models.get_cover_photo_path,
                    ),
                ),
                (
                    "address_line_1",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=20, null=True)),
                ("state", models.CharField(blank=True, max_length=20, null=True)),
                ("city", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must not consist of space and requires country code. eg : +6591258565",
                                regex="^(\\+\\d{1,3})?,?\\s?\\d{8,13}",
                            )
                        ],
                    ),
                ),
                ("postal_code", models.CharField(blank=True, max_length=6, null=True)),
                ("latitude", models.CharField(blank=True, max_length=20, null=True)),
                ("longitude", models.CharField(blank=True, max_length=20, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
