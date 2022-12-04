from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User


class AdminUser(UserAdmin):
    # model=User
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    ]
    list_display_links = ["id", "email", "username"]
    list_filter = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    readonly_fields = ["date_joined", "last_login", "created_date", "modified_date"]
    fieldsets = (
        ("Password", {"fields": ("password",)}),
        (
            "Personal Information",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("User Type", {"fields": ("role",)}),
        (
            "Permissions and Groups",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {"fields": ("last_login", "date_joined", "created_date", "modified_date")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_admin",
                    "is_superuser",
                ),
            },
        ),
    )



admin.site.register(User, AdminUser)
