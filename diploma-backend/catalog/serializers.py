from rest_framework import serializers
from .models import Product, Category, Tag, ProductImage, Review


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
        sub_categories = obj.subcategories.all()
        return CategorySerializer(sub_categories, many=True).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ReviewSerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(source='created_at', format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = TagSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    reviewsCount = serializers.IntegerField(source='reviews.count', read_only=True)

    freeDelivery = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "count",
            "date",
            "description",
            "full_description",
            "freeDelivery", 
            "reviews",
            "rating",
            "category",
            "tags",
            "images",
            "reviewsCount",
        ]

    def get_freeDelivery(self, obj):
        return obj.price > 2000

    def get_images(self, obj):
        request = self.context.get("request")
        result = []

        for img in obj.images.all():
            url = img.image.url
            if request:
               url = request.build_absolute_uri(url)
            result.append({"src": url, "alt": img.alt or obj.title})

        return result


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.ImageField(source="image")

    class Meta:
        model = ProductImage
        fields = ("src", "alt")




