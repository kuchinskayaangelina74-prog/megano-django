from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, BasketItem, CustomerOrder, OrderItem, Category, Tag


def index(request):
    return render(request, "frontend/index.html")


def api_index(request):
    products = Product.objects.all()[:8]

    items = []

    for p in products:
        items.append({
            "id": p.id,
            "title": p.title,
            "price": float(p.price),
            "images": [
                {
                    "src": request.build_absolute_uri(p.image.url) if p.image else "/static/frontend/assets/img/content/home/card.jpg",
                    "alt": p.title
                }
            ]
        })

    return JsonResponse({
        "popular": items,
        "limited": items,
        "banners": items
    })
    

def catalog(request):
    products = Product.objects.all()

    return render(
        request,
        "frontend/catalog.html",
        {
            "products": products
        }
    )


def api_catalog(request):
    search = request.GET.get("search")
    products = Product.objects.all()

    if search:
        products = products.filter(title__icontains=search)
    data = []

    for product in products:
        data.append({
            "id": product.id,
            "title": product.title,
            "price": float(product.price),
            "images": [
                {
                    "src": request.build_absolute_uri(product.image.url) if product.image else "/static/frontend/assets/img/content/home/card.jpg",
                    "alt": product.title
                }
            ]
        })

    return JsonResponse({
        "items": data,
        "currentPage": 1,
        "lastPage": 1
    })


def api_product(request, id):
    product = Product.objects.get(id=id)

    data = {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": float(product.price),
        "stock": product.stock,
        "images": [
            {
                "src": request.build_absolute_uri(product.image.url) if product.image else "/static/frontend/assets/img/content/home/card.jpg",
                "alt": product.title
            }
        ]
    }

    return JsonResponse(data)


@csrf_exempt
def api_basket(request):

    if request.method == "GET":

        items = BasketItem.objects.all()
        data = []

        for item in items:
            data.append({
                "id": item.product.id,
                "title": item.product.title,
                "price": float(item.product.price),
                "count": item.count,
                "images": [
                    {
                        "src": request.build_absolute_uri(item.product.image.url)
                        if item.product.image
                        else "/static/frontend/assets/img/content/home/card.jpg",
                        "alt": item.product.title
                    }
                ]
            })

        return JsonResponse(data, safe=False)


    if request.method == "POST":

        body = json.loads(request.body)
        product_id = body.get("id")
        count = body.get("count", 1)

        product = Product.objects.get(id=product_id)
        item, created = BasketItem.objects.get_or_create(product=product)

        if not created:
            item.count += count
        else:
            item.count = count

        item.save()

        return JsonResponse({"status": "added"})


    if request.method == "DELETE":

        body = json.loads(request.body)
        product_id = body.get("id")

        BasketItem.objects.filter(product_id=product_id).delete()

        return JsonResponse({"status": "deleted"})


@csrf_exempt
def api_orders(request):

    if request.method == "GET":

        orders = CustomerOrder.objects.all()

        data = []

        for order in orders:

            items = []
            for item in order.items.all():
                items.append({
                    "title": item.product.title,
                    "price": float(item.price),
                    "count": item.count
                })

            data.append({
                "id": order.id,
                "name": order.name,
                "email": order.email,
                "address": order.address,
                "created_at": order.created_at,
                "items": items
            })

        return JsonResponse(data, safe=False)


    if request.method == "POST":

        body = json.loads(request.body)

        name = body.get("name")
        email = body.get("email")
        address = body.get("address")

        basket_items = BasketItem.objects.all()

        order = CustomerOrder.objects.create(
            name=name,
            email=email,
            address=address
        )

        for item in basket_items:

            order_item = OrderItem.objects.create(
                product=item.product,
                count=item.count,
                price=item.product.price
            )

            order.items.add(order_item)
        basket_items.delete()

        return JsonResponse({"status": "order created", "orderId": order.id})


def api_categories(request):
    categories = Category.objects.all()
    data = []

    for cat in categories:
        data.append({
            "id": cat.id,
            "title": cat.title,
            "image": request.build_absolute_uri(cat.image.url) if cat.image else ""
        })

    return JsonResponse(data, safe=False)


def api_tags(request):
    tags = Tag.objects.all()
    data = []

    for tag in tags:
        data.append({
            "id": tag.id,
            "name": tag.name
        })

    return JsonResponse(data, safe=False)


def api_products_popular(request):
    products = Product.objects.all()[:8]

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "title": p.title,
            "price": float(p.price),
            "images": [
                {
                    "src": request.build_absolute_uri(p.image.url) if p.image else "/static/frontend/assets/img/content/home/card.jpg",
                    "alt": p.title
                }
            ]
        })

    return JsonResponse(data, safe=False)


def api_products_limited(request):
    products = Product.objects.all()[:8]

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "title": p.title,
            "price": float(p.price),
            "images": [
                {
                    "src": request.build_absolute_uri(p.image.url) if p.image else "/static/frontend/assets/img/content/home/card.jpg",
                    "alt": p.title
                }
            ]
        })

    return JsonResponse(data, safe=False)


def api_banners(request):
    products = Product.objects.all()[:3]

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "title": p.title,
            "price": float(p.price),
            "images": [
                {
                    "src": request.build_absolute_uri(p.image.url) if p.image else "/static/frontend/assets/img/content/home/card.jpg",
                    "alt": p.title
                }
            ]
        })

    return JsonResponse(data, safe=False)