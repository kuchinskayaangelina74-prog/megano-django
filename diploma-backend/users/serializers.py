from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    def get_avatar(self, obj):
        if obj.avatar:
            return {
                "src": obj.avatar.url,
                "alt": obj.fullName or "avatar"
            }
        return {"src": "", "alt": ""}


class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]

class PasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)