from django.conf import settings

from rest_framework import authentication, exceptions
import jwt

from . import models


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise exceptions.AuthenticationFailed("Unauthorized")

        try:
            payload = jwt.decode(token, settings.JWT_SECRETE, algorithms=["HS256"])

        except:
            raise exceptions.AuthenticationFailed("Unauthorized")

        user = models.User.objects.filter(id=payload["id"]).first()

        return (user, None)
