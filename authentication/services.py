from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from reports.models import Category
from reports.services import ReportService

from users.models import User
from users.serializers import UserSerializer


class AuthenticationService:
    @staticmethod
    def create_user(**data) -> User:
        """
        Create a new user.
        """
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        is_active = data.get("is_active", True)

        username = email.split("@")[0]

        is_admin = data.get("is_admin", False)
        admin_category_id = data.get("admin_category_id")

        if is_admin and not admin_category_id:
            raise ValidationError("Admin category is required for admin users.")

        if admin_category_id:
            admin_category = ReportService.get_category(id=admin_category_id)
        else:
            admin_category = None

        signup_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": username,
            "password": password,
            "phone": phone,
            "is_admin": is_admin,
            "admin_category": admin_category,
            "is_active": is_active,
        }

        try:
            user = User.objects.create_user(**signup_data)
        except Exception as e:
            # TODO: Log the error.
            raise ValidationError("Error creating user. Please try again.")

        return user

    @staticmethod
    def sign_in(**data) -> User:
        """
        Sign in a user.
        """
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed(
                "Incorrect email or password.",
            )

        return user

    @staticmethod
    def make_auth_response_data(user: User) -> dict:
        """
        Make an auth response data that contains the required
        auth credentials to be sent to the client.
        """
        serializer = UserSerializer(user)
        data = dict(serializer.data)

        auth_tokens = user.auth_tokens
        data["token"] = auth_tokens["access"]
        data["refresh"] = auth_tokens["refresh"]

        update_last_login(None, user)

        return data
