# Generated by Django 4.1.3 on 2022-12-19 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0006_category_fooditem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fooditem",
            old_name="title",
            new_name="name",
        ),
    ]