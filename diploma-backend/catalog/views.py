from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Create your views here.
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category").prefetch_related("tags")

        category = self.request.GET.get("category")
        if category and category != "0":
            queryset = queryset.filter(category__id=category)

        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort)

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
            })

        return Response({"items": items})


class LimitedProductsView(APIView):

    def get(self, request):
        products = Product.objects.order_by("-created_at")[:3]

        items = []
        for p in products:
            items.append({
                "id": p.id,
                "title": p.title,
                "price": float(p.price),
            })

        return Response({"items": items})
    

class BannersView(APIView):

    def get(self, request):
        products = Product.objects.all()[:3]

        items = [
            {
                "id": p.id,
                "title": p.title,
                "price": float(p.price),
                "image": p.image.url if p.image else None,
            }
            for p in products
        ]

        return Response({"items": items})


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer