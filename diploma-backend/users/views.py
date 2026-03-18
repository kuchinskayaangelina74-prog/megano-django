from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class ProfileView(APIView):
    def get(self, request):
        return Response({
            "name": "Test User",
            "email": "test@example.com"
        })

    def post(self, request):
        return Response({
            "status": "profile updated"
        })