from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Product
from .models import Order, OrderItem, Basket, BasketItem
# Create your views here.


class BasketView(APIView):

    def get(self, request):
        items = []
        total = 0

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_items = basket.items.all()

            for item in basket_items:
                product = item.product
                item_total = float(product.price) * item.count
                total += item_total

                items.append({
                    "id": product.id,
                    "title": product.title,
                    "price": float(product.price),
                    "count": item.count,
                    "total": item_total,
                    "image": product.image.url,
                })

        else:
            basket = request.session.get("basket", {})

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
                    "image": product.image.url,
                })
        
        return Response({
            "items": items,
            "total": total,
        })

    def post(self, request):
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)

            item, created = BasketItem.objects.get_or_create(
                basket=basket,
                product_id=product_id
            )

            if not created:
                item.count += count
            else:
                item.count = count

            item.save()

        else:
            basket = request.session.get("basket", {})
            product_id = str(product_id)

            if product_id in basket:
                basket[product_id] += count
            else:
                basket[product_id] = count

            request.session["basket"] = basket

        return Response({"result": "added"})

    def delete(self, request):
        product_id = request.data.get("id")

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            BasketItem.objects.filter(basket=basket, product_id=product_id).delete()
        else:
            basket = request.session.get("basket", {})
            product_id = str(product_id)

            if product_id in basket:
                del basket[product_id]

            request.session["basket"] = basket

        return Response({"result": "deleted"})


class OrderView(APIView):

    def get(self, request):
        user = request.user

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
        user = request.user 

        total = 0
        order = Order.objects.create(user=user, total_price=0)

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            items = basket.items.all()

            if not items:
                return Response({"error": "Basket is empty"}, status = 400)

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    count=item.count
                )
                total += item.product.price * item.count

            basket.items.all().delete()

        else:
            basket = request.session.get("basket", {})

            if not basket:
                return Response({"error": "Basket is empty"}, status=400)

            for product_id, count in basket.items():
                product = Product.objects.get(id=product_id)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    count=count
                )

                total += product.price * count

            request.session["basket"] = {}

        order.total_price = total
        order.save()

        return Response({
            "status": "order created",
            "order_id": order.id
        })


