from django.urls import path
from .views import SignInView, SignUpView, SignOutView, ProfileView


urlpatterns = [
    path("sign-in/", SignInView.as_view()),
    path("sign-up/", SignUpView.as_view()),
    path("sign-out/", SignOutView.as_view()),
    path("profile/", ProfileView.as_view()),
]