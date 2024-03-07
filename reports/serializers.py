from rest_framework import serializers

from reports.models import Category, Report
from users.serializers import MiniUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class SubmitReportSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    longitude = serializers.DecimalField(
        max_digits=22,
        decimal_places=16,
        required=False,
    )
    latitude = serializers.DecimalField(
        max_digits=22,
        decimal_places=16,
        required=False,
    )


class ReportSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = (
            "id",
            "status",
            "description",
            "location",
            "longitude",
            "latitude",
            "category",
            "user",
            "created_at",
        )
        read_only_fields = (
            "id",
            "status",
            "description",
            "location",
            "longitude",
            "latitude",
            "created_at",
        )


class ChangeCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=True)
