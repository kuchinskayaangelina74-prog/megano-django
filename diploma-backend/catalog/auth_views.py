from rest_framework.views import APIView
from rest_framework.response import Response


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