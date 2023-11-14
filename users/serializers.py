from rest_framework import serializers

from users.models import User

from reports.serializers import CategorySerializer


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
            "is_active",
        )
        read_only_fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
        )
