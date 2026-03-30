from django.contrib import admin
from .models import Category, Product, Tag, ProductImage
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category")
    list_filter = ("category", "tags")
    search_fields = ("title",)
    inlines = [ProductImageInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

