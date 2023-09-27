from django.urls import path

from . import views as apis


urlpatterns = [
    path("", apis.ShopApi.as_view(), name="shop create"),
    path(
        "<str:shop_id>/",
        apis.UpdateRetreiveDeleteShopApi.as_view(),
        name="Update Retreive Get",
    ),
]
