from django.urls import path

from . import views as apis

urlpatterns = [
    path("register/", apis.UserRegistrationApi.as_view(), name="register"),
    path("verify-email/", apis.VerifyEmailApi.as_view(), name="verify-email"),
]
