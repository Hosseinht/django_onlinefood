# Generated by Django 4.1.3 on 2022-12-09 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(1, "Restaurant"), (2, "Customer")], null=True
            ),
        ),
    ]
