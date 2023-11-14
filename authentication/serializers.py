from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8)
    admin_category_id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "is_admin",
            "admin_category_id",
        )


class SignInSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True)
