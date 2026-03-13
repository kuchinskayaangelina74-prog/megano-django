from rest_framework.views import APIView
from rest_framework.response import Response


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