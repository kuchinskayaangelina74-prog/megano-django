from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, PasswordUpdateSerializer
import json
# Create your views here.


class SignInView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SignUpView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        user.profile.fullName = data.get("name", "")
        user.profile.save()

        login(request, user)
        return Response(status=status.HTTP_201_CREATED)


class SignOutView(APIView):

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def post(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data["current_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(status=status.HTTP_200_OK)

            return Response({"error": "Wrong current password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        avatar = request.FILES.get("avatar")
        if avatar:
            profile.avatar = avatar
            profile.save()
            return Response(status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)