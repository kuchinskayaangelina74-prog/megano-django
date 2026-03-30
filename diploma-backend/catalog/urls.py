from django.urls import path
from .views import ProductListView, ProductDetailView, PopularProductsView, LimitedProductsView, BannersView, CategoryListView


urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    
    path("products/popular/", PopularProductsView.as_view()),
    path("products/limited/", LimitedProductsView.as_view()),
    
    path("banners/", BannersView.as_view()),
    path("categories/", CategoryListView.as_view()),
]