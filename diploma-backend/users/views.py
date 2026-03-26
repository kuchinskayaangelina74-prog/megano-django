from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class SignInView(APIView):

    def post(self, request):
        return Response({
            "token": "test-token"
        })


class SignUpView(APIView):

    def post(self, request):
        return Response({
            "status": "user created"
        })


class SignOutView(APIView):

    def post(self, request):
        return Response({
            "status": "logged out"
        })


class ProfileView(APIView):

    def get(self, request):
        return Response({
            "fullName": "Test User",
            "email": "test@test.com"
        })

    def post(self, request):
        return Response({
            "status": "profile updated"
        })