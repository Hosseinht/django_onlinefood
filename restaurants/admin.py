from django.contrib import admin

from .models import Category, FoodItem, Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["user_name", "restaurant_name", "is_approved", "created_at"]
    list_display_links = ["user_name", "restaurant_name"]
    list_editable = ["is_approved"]

    def restaurant_name(self, obj):
        return obj.name


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name", "restaurant"]
    search_fields = ["name", "restaurant__name"]


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name", "category", "restaurant", "price", "is_available"]
    search_fields = ["name"]
    list_filter = ["is_available"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
