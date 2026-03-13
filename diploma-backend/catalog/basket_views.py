from rest_framework.views import APIView
from rest_framework.response import Response


class BasketView(APIView):

    def get(self, request):
        return Response({"items": []})

    def post(self, request):
        return Response({"result": "added"})

    def delete(self, request):
        return Response({"result": "deleted"})