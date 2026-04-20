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
            basket_items = basket.items.select_related("product").all()

            for item in basket_items:
                product = item.product
                first_image = product.images.first()
                img_url = request.build_absolute_uri(first_image.image.url) if first_image else ""

                items.append({
                    "id": product.id,
                    "title": product.title,
                    "price": float(product.price),
                    "count": item.count,
                    "images": [
                        {
                            "src": img_url,
                            "alt": product.title,
                        }
                    ],
                })

        else:
            basket = request.session.get("basket", {})
            for product_id, count in basket.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    first_image = product.images.first()
                    img_url = request.build_absolute_uri(first_image.image.url) if first_image else ""
                
                    items.append({
                        "id": product.id,
                        "title": product.title,
                        "price": float(product.price),
                        "count": int(count),
                        "images": [
                            {
                                "src": img_url,
                                "alt": product.title,
                            }
                        ],
                    })
                except (Product.DoesNotExist, ValueError, TypeError):
                    continue
            
        return Response(items)

    def post(self, request):
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            item, created = BasketItem.objects.get_or_create(basket=basket, product_id=product_id)
            if not created:
                item.count += count
            else:
                item.count = count
            item.save()
        else:
            basket = request.session.get("basket", {})
            basket[str(product_id)] = basket.get(str(product_id), 0) + count
            request.session["basket"] = basket

        return self.get(request)

    def delete(self, request):
        product_id = request.data.get("id")

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            BasketItem.objects.filter(basket=basket, product_id=product_id).delete()
        else:
            basket = request.session.get("basket", {})
            if str(product_id) in basket:
                del basket[str(product_id)]

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
                    "createdAt": order.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(order, 'created_at') else "2025-04-16 18:00",
                    "fullName": request.user.get_full_name() or request.user.username,
                    "email": request.user.email,
                    "phone": getattr(request.user.profile, 'phone', ""),
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
                "totalCost": float(order.total_price),
                "status": order.status,
                "products": [{"id": i.product.id, "title": i.product.title} for i in order.items.all()]
            })
        return Response(data)
            
    def post(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Auth required"}, status=401)

        if pk:
            try:
                order = Order.objects.get(id=pk, user=request.user)
                order.save()
                return Response({"orderId": order.id})

            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=404)

        user = request.user
        basket, _ = Basket.objects.get_or_create(user=request.user)
        items = basket.items.all()

        if not items.exists():
            return Response({"error": "Basket is empty"}, status=400)

        order = Order.objects.create(user=request.user, total_price=0, status="created")
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
        number = str(request.data.get("number", "")).replace(" ", "")

        if not order_id or not number.isdigit():
            return Response({"error": "Invalid data"}, status=400)
        
        try:
            order = Order.objects.get(id=order_id)
            num = int(number)
            if num % 2 == 0 and not number.endswith("0"):
                order.status = "paid"
            else:
                order.status = "failed"
            order.save()

            return Response({"status": order.status})
        except Order.DoesNotExist:

            return Response({"error": "Order not found"}, status=404)

