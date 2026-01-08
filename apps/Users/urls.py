from django.urls import path
from .views import UserSignUp, UserSignIn, UserProfile

urlpatterns = [
    path("signup/", UserSignUp.as_view(), name="user_signup"),
    path("signin/", UserSignIn.as_view(), name="user_signin"),
    path("profile/", UserProfile.as_view(), name="user_profile"),
]