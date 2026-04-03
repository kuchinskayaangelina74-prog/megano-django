from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Product
from .models import Order, OrderItem
# Create your views here.


class BasketView(APIView):

    def get(self, request):
        basket = request.session.get("basket", {})

        items = []
        total = 0
        for product_id, count in basket.items():
            product = Product.objects.get(id=product_id)

            item_total = float(product.price) * count
            total += item_total

            items.append({
                "id": product.id,
                "title": product.title,
                "price": float(product.price),
                "count": count,
                "total": item_total,
            })
        return Response({
            "items": items,
            "total": total,
            "basket": {
                "items": items,
                "total": total
            }
        })

    def post(self, request):
        product_id = str(request.data.get("id"))
        count = int(request.data.get("count", 1))

        basket = request.session.get("basket", {})

        if product_id in basket:
            basket[product_id] += count
        else:
            basket[product_id] = count
        
        request.session["basket"] = basket
        return Response({"result": "added"})

    def delete(self, request):
        product_id = str(request.data.get("id"))

        basket = request.session.get("basket", {})

        if product_id in basket:
            del basket[product_id]

        request.session["basket"] = basket

        return Response({"result": "deleted"})


class OrderView(APIView):

    def get(self, request):
        user = User.objects.first() 

        orders = Order.objects.filter(user=user)

        data = []
        for order in orders:
            items = []
            for item in order.items.all():
                items.append({
                    "product": item.product.title,
                    "count": item.count
                })

            data.append({
                "id": order.id,
                "total": float(order.total_price),
                "items": items
            })

        return Response({"orders": data})


    def post(self, request):
        basket = request.session.get("basket", {})
        user = User.objects.first()  

        if not basket:
            return Response({"error": "Basket is empty"}, status=400)

        total = 0
        order = Order.objects.create(user=user, total_price=0)

        for product_id, count in basket.items():
            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                count=count
            )

            total += product.price * count

        order.total_price = total
        order.save()

        request.session["basket"] = {}

        return Response({
            "status": "order created",
            "order_id": order.id
        })
