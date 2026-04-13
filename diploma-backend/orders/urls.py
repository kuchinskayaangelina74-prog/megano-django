from django.urls import path
from .views import BasketView, OrderView, PaymentView


urlpatterns = [
     path("basket/", BasketView.as_view()),
     path("", OrderView.as_view()),
     path("payment/", PaymentView.as_view()),
] 