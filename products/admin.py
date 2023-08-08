from django.contrib import admin
from .models import Category, Tag, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
