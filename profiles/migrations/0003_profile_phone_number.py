# Generated by Django 4.1.3 on 2022-12-08 12:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_remove_profile_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(
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
    ]
