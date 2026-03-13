from rest_framework.views import APIView
from rest_framework.response import Response


class OrderView(APIView):

    def get(self, request):
        return Response({
            "orders": []
        })

    def post(self, request):
        return Response({
            "orderId": 1
        })