from django.urls import path
from .views import ProductListView, ProductDetailView, PopularProductsView, LimitedProductsView, BannersView
from .basket_views import BasketView
from .order_views import OrderView
from .profile_views import ProfileView
from .auth_views import SignInView, SignUpView, SignOutView

urlpatterns = [
    path("catalog/", ProductListView.as_view(), name="catalog"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("basket/", BasketView.as_view(), name="basket"),
    path("orders/", OrderView.as_view(), name="orders"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("sign-in/", SignInView.as_view(), name="signin"),
    path("sign-up/", SignUpView.as_view(), name="signup"),
    path("sign-out/", SignOutView.as_view(), name="signout"),
    path("products/popular/", PopularProductsView.as_view()),
    path("products/limited/", LimitedProductsView.as_view()),
    path("banners/", BannersView.as_view()),
]