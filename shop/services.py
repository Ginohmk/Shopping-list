import dataclasses
import datetime
from typing import TYPE_CHECKING
from user import services as user_services
from . import models


if TYPE_CHECKING:
    from .models import Shop
    from user.models import User


@dataclasses.dataclass
class ShopDataClass:
    title: str
    priority: int
    due_date: datetime.datetime
    description: str
    quantity: int
    id: str = None
    created_at: datetime.datetime = None
    user: user_services.UserDataClass = None
    is_complete: bool = False

    @classmethod
    def from_instance(cls, shop: "Shop") -> "ShopDataClass":
        return cls(
            id=shop.id,
            title=shop.title,
            priority=shop.priority,
            description=shop.description,
            due_date=shop.due_date,
            created_at=shop.created_at,
            quantity=shop.quantity,
            is_complete=shop.is_complete,
            user=shop.user,
        )


def create_shop(user: "User", shop: "Shop") -> "ShopDataClass":
    shop = models.Shop(
        title=shop.title,
        priority=shop.priority,
        description=shop.description,
        due_date=shop.due_date,
        created_at=shop.created_at,
        quantity=shop.quantity,
        is_complete=shop.is_complete,
        user=user,
    )

    shop.save()

    return ShopDataClass.from_instance(shop)


def get_user_shop_list(user_details: "User") -> list["ShopDataClass"]:
    shop_list = models.Shop.objects.filter(user=user_details)

    return [ShopDataClass.from_instance(single_shop) for single_shop in shop_list]
