from rest_framework import serializers
from .models import Product, Category, Tag, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields =  ["id", "title", "image", "subcategories"]

    def get_image(self, obj):
        if obj.image:
            return {
                "src": obj.image.url,
                "alt": obj.title
            }
        return {
            "src": "",
            "alt": ""
        }

    def get_subcategories(self, obj):
        return []


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.ImageField(source="image")

    class Meta:
        model = ProductImage
        fields = ("src", "alt")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "category",
            "tags",
            "images",
        ]








