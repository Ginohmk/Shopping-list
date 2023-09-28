from django.shortcuts import render
from rest_framework import views, response, status, exceptions
from . import serializers as user_serializer
from . import services
from . import user_permissions
from . import user_authentications
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
        user = services.check_user_email(user_data.email)

        if user:
            raise exceptions.NotAcceptable("Email already exist")

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

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class VerifyEmailApi(views.APIView):
    def post(self, request):
        token = request.GET.get("token")

        user_data = services.verify_email_auth(token)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        serializer = user_serializer.UserSerializer(user_data)

        resp.data = serializer.data
        resp.status_code = status.HTTP_202_ACCEPTED

        return resp


class LoginApi(views.APIView):


    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user_data = services.check_user_email(email)

        if user_data is None:
            raise exceptions.AuthenticationFailed("Wrong credentials provided")

        if not user_data.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Wrong credentials provided")

        # Token
        token = services.generate_token(user_data.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        resp.status_code = status.HTTP_204_NO_CONTENT

        return resp


class LogoutApi(views.APIView):
    authentication_classes = (user_authentications.CustomUserAuthentication,)
    permission_classes = (user_permissions.CustomPermision,)

    def post(self, request):
        res = response.Response()

        print(request.user)

        res.delete_cookie("jwt")
        res.data = {"message": "Logged out is Successfull"}
        res.status_code = status.HTTP_204_NO_CONTENT
        return res


class UserApi(views.APIView):
    """
    description: Endpoint to get current login user

    return: user: json
    """

    authentication_classes = (user_authentications.CustomUserAuthentication,)
    permission_classes = (user_permissions.CustomPermision,)

    def get(self, request):
        user = request.user

        serializer = user_serializer.UserSerializer(user)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
