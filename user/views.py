from django.shortcuts import render
from rest_framework import views, response, status
from . import serializers as user_serializer
from . import services

from django.conf import settings

# For email sending
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class UserRegistrationApi(views.APIView):
    def post(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data

        # Check if email exist in db
        services.check_user_email(user_data.email)

        serializer.instance = services.create_user(user_data)

        #  Generate User Token for Email verification
        token = services.generate_token(serializer.data.get("id"))

        current_site = settings.USER_ENVIRONMENT
        relative_link = reverse("verify-email")
        abs_url = current_site + relative_link + "?token=" + str(token)
        email_body = f'Hi {serializer.data.get("first_name")} {serializer.data.get("last_name")}, Please use the link below to verify your email. \n {abs_url} '
        email_info = {
            "subject": "Verify your email",
            "body": email_body,
            "user_email": serializer.data.get("email"),
        }

        services.send_email(email_info)

        return response.Response(data=serializer.data)


class VerifyEmailApi(views.APIView):
    def post(self, request):
        token = request.GET.get("token")

        user_data = services.verify_email_auth(token)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        serializer = user_serializer.UserSerializer(user_data)

        resp.data = serializer.data

        return resp
