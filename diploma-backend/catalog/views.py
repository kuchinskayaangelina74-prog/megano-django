from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Count

# Create your views here.
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category").prefetch_related("tags", "images", "reviews")

        search = self.request.GET.get("filter[name]")
        if search:
            queryset = queryset.filter(title__icontains=search)

        category = self.request.GET.get("filter[category]")
        if category:
            queryset = queryset.filter(category__id=category)

        min_price = self.request.GET.get("filter[minPrice]")
        max_price = self.request.GET.get("filter[maxPrice]")

        if min_price:
           queryset = queryset.filter(price__gte=min_price)

        if max_price:
           queryset = queryset.filter(price__lte=max_price)

        tags = self.request.GET.getlist("filter[tags][]")
        if tags:
            queryset = queryset.filter(tags__id__in=tags).distinct()

        sort = self.request.GET.get("sort")
        sort_type = self.request.GET.get("sortType")

        if sort:
            if sort == 'reviews':
                
                queryset = queryset.annotate(reviews_count=Count('reviews'))
                sort = 'reviews_count'

            if sort == 'rating':
                return sorted(queryset, key=lambda p: p.rating, reverse=(sort_type == "dec"))

            if sort_type == "dec":
                sort = f"-{sort}"
            queryset = queryset.order_by(sort)

        return queryset


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related("category").prefetch_related("tags", "images", "reviews")
    serializer_class = ProductSerializer


class PopularProductsView(APIView):

    def get(self, request):
        products = list(Product.objects.filter(archived=False))
        products = sorted(products, key=lambda p: p.rating, reverse=True)[:8]
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class LimitedProductsView(APIView):

    def get(self, request):
        products = Product.objects.filter(is_limited_edition=True).order_by("-date")[:8]
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    

class BannersView(APIView):

    def get(self, request):
        products = Product.objects.filter(is_banner=True)[:3]
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


class ReviewView(APIView):

    def post(self, request, pk):
        product = Product.objects.get(id=pk)

        Review.objects.create(
            product=product,
            author=request.data.get("author"),
            email=request.data.get("email"),
            text=request.data.get("text"),
            rate=request.data.get("rate"),
        )
        
        return Response({"status": "review added"})


class SalesView(APIView):

    def get(self, request):
        products = Product.objects.filter(price__lt=5000)[:10] 
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)