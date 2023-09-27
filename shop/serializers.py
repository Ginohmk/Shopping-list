from rest_framework import serializers
from user.serializers import UserSerializer
from . import services


class ShopSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    description = serializers.CharField()
    priority = serializers.IntegerField()
    title = serializers.CharField()
    due_date = serializers.DateTimeField()
    quantity = serializers.IntegerField()
    is_complete = serializers.BooleanField(read_only=True)
    user = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.ShopDataClass(**data)
