from django.contrib import admin

from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["user_name", "restaurant_name", "is_approved", "created_at"]
    list_display_links = ["user_name", "restaurant_name"]
    list_editable = ["is_approved"]

    def restaurant_name(self, obj):
        return obj.name


admin.site.register(Restaurant, RestaurantAdmin)
