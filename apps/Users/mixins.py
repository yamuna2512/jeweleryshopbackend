from rest_framework import status
from django.utils import timezone
from config.helpers.error_response import error_response
from .models import User
class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check Authorization header
        token = request.headers.get("Authorization")
        if not token:
            return error_response(
                "Please set Auth-Token in Authorization header.",
                status.HTTP_401_UNAUTHORIZED
            )
        #  Validate token and expiration
        now = timezone.now()
        try:
            user = User.objects.get(token=token, token_expires__gt=now)
        except User.DoesNotExist:
            return error_response(
                "The token is invalid or expired.",
                status.HTTP_401_UNAUTHORIZED
            )
        #  Attach user to request so views can use it
        request.login_user = user
        #Allow request to continue
        return super().dispatch(request, *args, **kwargs)