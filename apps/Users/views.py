
from rest_framework import generics
from rest_framework.response import Response
from apps.Users.mixins import CustomLoginRequiredMixin
from .models import User
from .serializers import UserSerializer, UserSignInSerializer, UserSignUpSerializer


class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

class UserSignIn(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignInSerializer

class UserProfile(CustomLoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.login_user)
        return Response(serializer.data)