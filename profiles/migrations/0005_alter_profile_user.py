# Generated by Django 4.1.3 on 2022-12-15 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("profiles", "0004_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
