from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Create your views here.
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category").prefetch_related("tags", "images")

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        category = self.request.GET.get("category")
        if category and category != "0":
            queryset = queryset.filter(category__id=category)

        min_price = self.request.GET.get("minPrice")
        max_price = self.request.GET.get("maxPrice")

        if min_price:
           queryset = queryset.filter(price__gte=min_price)

        if max_price:
           queryset = queryset.filter(price__lte=max_price)

        tags = self.request.GET.getlist("tags")
        if tags:
            queryset = queryset.filter(tags__id__in=tags).distinct()

        sort = self.request.GET.get("sort")
        if sort:
            if sort == "price":
                queryset = queryset.order_by("price")
            elif sort == "-price":
                queryset = queryset.order_by("-price")
            
            elif sort == "reviews":
                queryset = queryset.order_by("-id")

        return queryset


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related("category").prefetch_related("tags")
    serializer_class = ProductSerializer


class PopularProductsView(APIView):

    def get(self, request):
        products = Product.objects.order_by("-created_at")[:3]

        items = []
        for p in products:
            items.append({
                "id": p.id,
                "title": p.title,
                "price": float(p.price),
                "images": [
                    {
                        "src": request.build_absolute_uri(img.image.url),
                        "alt": img.alt
                    }
                    for img in p.images.all()
                ] if  p.images.exists() else (
                    [
                        {
                            "src": request.build_absolute_uri(p.image.url),
                            "alt": p.title
                        }
                    ]if p.image else []
                )
            })

        return Response(items)


class LimitedProductsView(APIView):

    def get(self, request):
        products = Product.objects.order_by("-created_at")[:3]

        items = []
        for p in products:
            items.append({
                "id": p.id,
                "title": p.title,
                "price": float(p.price),
                "images": [
                    {
                        "src": request.build_absolute_uri(img.image.url),
                        "alt": img.alt
                    }
                    for img in p.images.all()
                ] if p.images.exists() else (
                    [
                        {
                            "src": request.build_absolute_uri(p.image.url),
                            "alt": p.title
                        }
                    ] if p.image else []
                )
            })

        return Response(items)
    

class BannersView(APIView):

    def get(self, request):
        products = Product.objects.select_related("category").prefetch_related("images", "tags").all()[:3]

        items = [
            {
                "id": p.id,
                "title": p.title,
                "price": float(p.price),
                "images": [
                    {
                        "src": request.build_absolute_uri(img.image.url),
                        "alt": img.alt
                    }
                    for img in p.images.all()
                ] if p.images.exists() else (
                    [
                        {
                            "src":request.build_absolute_uri(p.image.url),
                            "alt": p.title
                        }
                    ] if p.image else []
                )
            }
            for p in products
        ]

        return Response(items)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer





    