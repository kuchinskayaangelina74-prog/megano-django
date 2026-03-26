from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Product
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
        return Response({
            "orders": []
        })

    def post(self, request):
        return Response({
            "status": "ok"
        })