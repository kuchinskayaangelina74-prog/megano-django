from django.urls import path
from .views import(
    ProductListView, 
    ProductDetailView, 
    PopularProductsView, 
    LimitedProductsView, 
    BannersView, 
    CategoryListView, 
    ReviewView, 
    SalesView
)


urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/reviews/", ReviewView.as_view()),
    
    path("products/popular/", PopularProductsView.as_view()),
    path("products/limited/", LimitedProductsView.as_view()),
    
    path("banner/", BannersView.as_view()),
    path("categories/", CategoryListView.as_view()),
    path("sales/", SalesView.as_view()),

] 