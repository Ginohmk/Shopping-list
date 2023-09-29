import dataclasses
import datetime
from typing import TYPE_CHECKING
from user import services as user_services
from rest_framework import exceptions
from uuid import UUID
from . import models


if TYPE_CHECKING:
    from .models import Shop
    from user.models import User


####### Helper Function #######
def check_valid_uuid(id):
    try:
        UUID(id, version=4)

    except:
        raise exceptions.ValidationError("Id is not valid")


def update_delete_retreive_shop_checker(shop_instance, user_instance):
    if not shop_instance:
        raise exceptions.NotFound("Not found")

    if shop_instance.user != user_instance:
        raise exceptions.PermissionDenied("Unauthorize")


@dataclasses.dataclass
class ShopDataClass:
    """Defines the data struture of the user for response.

    Class varibles
    ----------
    title : str
        The user first name

    priority : str
        The user last name

    due_date : str
        The user email


    description : str, default None
        The user password


    Methods
    ------
    from_instance(cls, user)
        Returns object of class
    """

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
    """Create a shop saved to db

    Parameters
    ----------
    user : str
        user objects that needs to be saved in database

    shop_id : str
        Shop id to be updated

    Returns
    -------
      ShopDataClass object variables
    """

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
    """Get all shops owened by user

    Parameters
    ----------
    user : str
        user objects that needs to be saved in database

    shop_id : str
        Shop id to be updated

    Returns
    -------
      list of ShopDataClass object variables
    """

    shop_list = models.Shop.objects.filter(user=user_details)

    return [ShopDataClass.from_instance(single_shop) for single_shop in shop_list]


def get_user_shop_item(user: "User", shop_id: int) -> "ShopDataClass":
    """Get and display a  shop by id

    Parameters
    ----------
    user : str
        user objects that needs to be saved in database

    shop_id : str
        Shop id to be updated

    Returns
    -------
      ShopDataClass object variables
    """

    check_valid_uuid(shop_id)

    shop = models.Shop.objects.filter(id=shop_id).first()

    update_delete_retreive_shop_checker(shop, user)

    return ShopDataClass.from_instance(shop)


def delete_user_shop_item(user: "User", shop_id: str):
    """Delete shop by id

    Parameters
    ----------
    user : str
        user objects that needs to be saved in database

    shop_id : str
        Shop id to be updated

    Returns
    -------
      ShopDataClass object variables
    """

    check_valid_uuid(shop_id)

    shop = models.Shop.objects.filter(id=shop_id).first()

    update_delete_retreive_shop_checker(shop, user)

    shop.delete()


def update_user_shop_item(
    user: "User", shop_id: str, shop_data: "Shop"
) -> "ShopDataClass":
    """Update shop by  user to the database.

    Parameters
    ----------
    user : str
        user objects that needs to be saved in database

    shop_id : str
        Shop id to be updated

    shop_data : str
        Shop data contains efit information id


    Returns
    -------
      ShopDataClass object variables
    """
    check_valid_uuid(shop_id)

    shop = models.Shop.objects.filter(id=shop_id).first()

    update_delete_retreive_shop_checker(shop, user)

    shop.title = shop_data.title
    shop.is_complete = shop_data.is_complete
    shop.description = shop_data.description
    shop.priority = shop_data.priority
    shop.due_date = shop_data.due_date
    shop.quantity = shop_data.quantity

    shop.save()

    return ShopDataClass.from_instance(shop)
