
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password, check_password
from secrets import token_hex
from django.utils import timezone
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'token', 'token_expires')
class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)
    token_expires = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'token',
            'token_expires'
        )
    # Override create()
    def create(self, validated_data):
        # Check if email is taken
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'email': ['This email is already taken.']})
        # Hash password
        validated_data['password'] = make_password(validated_data['password'])
        # Generate token
        validated_data['token'] = token_hex(30)
        validated_data['token_expires'] = timezone.now() + timezone.timedelta(days=7)
        # Create user
        return super().create(validated_data)
class UserSignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    token_expires = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'token',
            'token_expires'
        )
    def validate(self, attrs):
        try:
            user = User.objects.get(email__iexact=attrs['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed("The password or email is incorrect.")

        if not check_password(attrs['password'], user.password):
            raise AuthenticationFailed("The password or email is incorrect.")

        self.user = user
        return attrs

    def create(self, validated_data):
        user = self.user
        user.token = token_hex(30)
        user.token_expires = timezone.now() + timezone.timedelta(days=7)
        user.save()
        return user