from django.contrib import admin

from .models import Category, FoodItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ['name', 'restaurant']
    search_fields = ['name', 'restaurant__name']


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'category', 'restaurant', 'price', 'is_available']
    search_fields = ['name']
    list_filter = ['is_available']


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
