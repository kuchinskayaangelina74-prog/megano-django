from django.contrib import admin
from .models import Category, Product, Tag, ProductImage, Review
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent")
    list_display_links = ("id", "title")
    fields = ("title", "parent", "image") 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "count", "category", "rating_display")
    list_filter = ("category", "tags", "is_limited_edition", "is_banner")
    search_fields = ("title", "description")
    inlines = [ProductImageInline]

    def rating_display(self, obj):
        return obj.rating
    rating_display.short_description = 'Рейтинг'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "author", "rate", "created_at")

