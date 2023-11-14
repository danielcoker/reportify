from rest_framework import serializers

from reports.models import Category, Report


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class ReportSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Report
        fields = (
            "id",
            "status",
            "description",
            "location",
            "category",
            "created_at",
        )
        read_only_fields = (
            "id",
            "status",
            "location",
            "created_at",
        )
