from django.urls import path

from . import views as apis


urlpatterns = [path("", apis.ShopApi.as_view(), name="shop create")]
