import dataclasses
from typing import TYPE_CHECKING
from rest_framework import exceptions
from django.conf import settings

# Encoding Jwt
import jwt
import datetime


# Emailing
from django.core.mail import EmailMessage

from . import models

if TYPE_CHECKING:
    from user.models import User


@dataclasses.dataclass
class UserDataClass:
    """Defines the data struture of the user for response.

    Class varibles
    ----------
    first_name : str
        The user first name

    last_name : str
        The user last name

    email : str
        The user email

    is_email_verified : bool, default None
        The user , if email is verified

    password : str, default None
        The user password

    id : str, default None
        The user id

    Methods
    ------
    from_instance(cls, user)
        Returns object of class
    """

    first_name: str
    last_name: str
    email: str
    is_email_verified: bool = None
    password: str = None
    id: str = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        """Structure user data reponse.

        Parameters
        ----------
        user : instance obj
            user objects that needs to be saved in database


        Returns
        -------
          UserDataClass object variables
        """
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_email_verified=user.is_email_verified,
            id=user.id,
        )


# Check User Email
def check_user_email(user_email: str) -> None:
    """Checks if user email already exist in the database.

    Parameters
    ----------
    email : str
        The email value to check if it exist or not in database

    Raises
    ------
    NotAcceptable
        If Email is already in the database.
    """

    user = models.User.objects.filter(email=user_email).first()

    return user


# Create User
def create_user(user: "UserDataClass") -> "UserDataClass":
    """Creates user by adding user to the database.

    Parameters
    ----------
    user : str
        user objects that needs to be saved in database

    Raises
    ------
    ValidationError
        If user password is None or Empty.

    Returns
    -------
      UserDataClass object variables
    """

    user_instance = models.User(
        first_name=user.first_name, last_name=user.last_name, email=user.email
    )

    if user.password is None:
        raise exceptions.ValidationError("Password can not be empty")

    user_instance.set_password(user.password)

    user_instance.save()

    return UserDataClass.from_instance(user_instance)


def generate_token(user_id: str) -> str:
    """Creates Token based on user id.

    Parameters
    ----------
    user_id : str
        user id to be encoded into token

    Raises
    ------
    ValidationError
        If user password is None or Empty.

    Returns
    -------
      token : str, object variables
    """

    payload = {
        "id": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.JWT_SECRETE, algorithm="HS256")

    return token


def send_email(data: dict) -> None:
    """Send Email to user.

    Parameters
    ----------
    data : object
        Email data to be sent

        Parameters
        -----------
          subject: str
          body: str
          user_email: str
    """

    email = EmailMessage(
        subject=data.get("subject"),
        body=data.get("body"),
        from_email=settings.EMAIL_HOST_USER,
        to=[data.get("user_email")],
    )
    email.send()


def verify_email_auth(token) -> "UserDataClass":
    """Verify user authentication of email.

    Parameters
    ----------
    token : str
        token  to be decoded

    Raises
    ------
    AuthenticationFailed
        If token password is None or Empty & when token is invalid.

    Returns
    -------
      token : UserDataClass, object insatnce of user

    """
    if not token:
        raise exceptions.AuthenticationFailed("Unauthorized")

    try:
        payload = jwt.decode(token, settings.JWT_SECRETE, algorithms=["HS256"])

        user = models.User.objects.filter(id=payload.get("id")).first()

        user.is_email_verified = True

        user.save()

        return UserDataClass.from_instance(user)

    except:
        raise exceptions.AuthenticationFailed("Unauthorized")
