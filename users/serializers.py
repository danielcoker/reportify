from rest_framework import serializers

from users.models import User
from reports.models import Category


# TODO: Refactor serializers to avoid circular imports.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class UserSerializer(serializers.ModelSerializer):
    admin_category = CategorySerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "phone",
            "is_active",
            "is_admin",
            "admin_category",
        )
        read_only_fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "phone",
            "is_active",
            "is_admin",
        )


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_active",
        )
        read_only_fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_active",
        )
