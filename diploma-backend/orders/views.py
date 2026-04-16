import json
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from catalog.models import Product
from .models import Order, OrderItem, Basket, BasketItem
# Create your views here.

class BasketView(APIView):

    def get(self, request):
        items = []

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_items = basket.items.all()

            for item in basket_items:
                product = item.product

                items.append({
                    "id": product.id,
                    "title": product.title,
                    "price": float(product.price),
                    "count": item.count,
                    "images": [
                        {
                            "src": request.build_absolute_uri(product.image.url)
                            if product.image
                            else "",
                            "alt": product.title,
                        }
                    ],
                })

        else:
            basket = request.session.get("basket", {})
            cleaned_basket = {}
            for product_id, count in basket.items():
        
                if product_id is None or count is None:
                    continue

                try:
                    product_id_int = int(product_id)
                    count_int = int(count)
                except (TypeError, ValueError):
                    continue

                if count_int <= 0:
                    continue

                try:
                    product = Product.objects.get(id=product_id_int)
                except (Product.DoesNotExist, TypeError, ValueError):
                    continue 
                
                items.append({
                    "id": product.id,
                    "title": product.title,
                    "price": float(product.price),
                    "count": count_int,
                    "images": [
                        {
                            "src": request.build_absolute_uri(product.image.url)
                            if product.image
                            else "",
                            "alt": product.title,
                        }
                    ],
                })
                cleaned_basket[str(product_id_int)] = count_int

            if cleaned_basket != basket:
                request.session["basket"] = cleaned_basket
        
        return Response(items)

    def post(self, request):
        payload = request.data 
        product_id = payload.get("id")
        count_raw = payload.get("count", 1)

        try:
            product_id_int = int(product_id)
        except (TypeError, ValueError):
            return self.get(request)

        try:
            count_int = int(count_raw)
        except (TypeError, ValueError):
            count_int = 1

        if product_id_int <= 0 or count_int <= 0:
            return self.get(request)
        
        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)

            item, created = BasketItem.objects.get_or_create(
                basket=basket,
                product_id=product_id_int
            )

            if not created:
                item.count += count_int
            else:
                item.count = count_int
            item.save()

        else:
            basket = request.session.get("basket", {})
            key = str(product_id_int)
            basket[key] = basket.get(key, 0) + count_int
            request.session["basket"] = basket

        return self.get(request)


    def delete(self, request):
        payload = request.data 
        product_id = payload.get("id")

        try:
            product_id_int = int(product_id)
        except (TypeError, ValueError):
                return self.get(request)

        if product_id_int <= 0:
            return self.get(request)

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            BasketItem.objects.filter(basket=basket, product_id=product_id_int).delete()
        else:
            basket = request.session.get("basket", {})
            key = str(product_id_int)

            if key in basket:
                del basket[key]

            request.session["basket"] = basket

        return self.get(request)


class OrderView(APIView):
    
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response([]) 

        if pk:
            try:
                order = Order.objects.get(id=pk, user=request.user)
                return Response({
                    "id": order.id,
                    "createdAt": "2025-04-16 18:00",
                    "fullName": request.user.get_full_name() or request.user.username,
                    "email": request.user.email,
                    "phone": "123456654321",
                    "deliveryType": "free",
                    "paymentType": "online",
                    "totalCost": float(order.total_price),
                    "status": order.status,
                    "city": "Moscow",
                    "address": "Arbat str.",
                    "products": [
                        {
                            "id": item.product.id,
                            "title": item.product.title,
                            "price": float(item.product.price),
                            "count": item.count,
                        } for item in order.items.all()
                    ]
                })
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=404)

        orders = Order.objects.filter(user=request.user)
        data = []

        for order in orders:
            data.append({
                "id": order.id,
                "createdAt": "2025-04-16 18:00",
                "fullName": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
                "phone": "123456654321",
                "deliveryType": "free",
                "paymentType": "online",
                "totalCost": float(order.total_price),
                "status": order.status,
                "products": [
                    {
                        "id": item.product.id,
                        "title": item.product.title,
                        "price": float(item.product.price),
                        "count": item.count,
                    } for item in order.items.all()
                ]
            })
        return Response(data)
            

    def post(self, request, pk=None):
        if pk:
            return Response({"orderId": pk})

        if not request.user.is_authenticated:
            return Response({"error": "Auth required"}, status=401)

        user = request.user 
        basket, _ = Basket.objects.get_or_create(user=user)
        items = basket.items.all()

        if not items.exists():
            return Response({"error": "Basket is empty"}, status=400)

        order = Order.objects.create(user=user, total_price=0, status="created")
        total = 0

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                count=item.count
            )
            total += item.product.price * item.count

        order.total_price = total
        order.save()
        items.delete()

        return Response({
            "orderId": order.id
        })


class PaymentView(APIView):

    def post(self, request, pk=None):
        order_id = pk or request.data.get("orderId")
        number = request.data.get("number")

        if not order_id or not number:
            return Response({"error": "Invalid data"}, status=400)
        
        number = str(number).replace(" ", "")

        if not number.isdigit() or len(number) > 16:
            return Response({"error": "Invalid number"}, status=400)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        number_int = int(number)
        if number_int % 2 == 0 and not str(number).endswith("0"):
            order.status = "paid"
        else:
            order.status = "failed"

        order.save()

        return Response({
            "status": order.status
        })