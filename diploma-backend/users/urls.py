from django.urls import path
from .views import SignInView, SignUpView, SignOutView, ProfileView, ProfilePasswordView, AvatarUpdateView


urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/password", ProfilePasswordView.as_view(), name="profile-password"),
    path("profile/avatar", AvatarUpdateView.as_view(), name="profile-avatar"),
]