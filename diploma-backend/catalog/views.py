from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category")

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__title=category)

        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort)

        return queryset


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer


class PopularProductsView(APIView):

    def get(self, request):
        products = Product.objects.all()[:3]

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
        products = Product.objects.all()[:3]

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
        return Response({
            "items": []
        })