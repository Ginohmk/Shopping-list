from django.shortcuts import render

from user import user_authentications, user_permissions

from . import services


from rest_framework import exceptions, views, response, status
from . import serializers as shop_serializer


class ShopApi(views.APIView):
    authentication_classes = (user_authentications.CustomUserAuthentication,)
    permission_classes = (user_permissions.CustomPermision,)

    def post(self, request):
        serializer = shop_serializer.ShopSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.create_shop(request.user, data)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        shop_data = services.get_user_shop_list(request.user)

        serializer = shop_serializer.ShopSerializer(shop_data, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class UpdateRetreiveDeleteShopApi(views.APIView):
    authentication_classes = (user_authentications.CustomUserAuthentication,)
    permission_classes = (user_permissions.CustomPermision,)

    def get(self, request, shop_id):
        shop_data = services.get_user_shop_item(request.user, shop_id)

        serializer = shop_serializer.ShopSerializer(shop_data)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, shop_id):
        services.delete_user_shop_item(request.user, shop_id)

        return response.Response(
            data={"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, shop_id):
        serializer = shop_serializer.ShopSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        shop_data = serializer.validated_data

        serializer.instance = services.update_user_shop_item(
            request.user, shop_id, shop_data
        )

        return response.Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
