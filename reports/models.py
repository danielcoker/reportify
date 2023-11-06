import uuid

from django.db import models

from core.models import SoftDeleteModel, TimestampedModel


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Report(TimestampedModel, SoftDeleteModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.TextField()
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="reports",
    )

    def __str__(self):
        return self.id.hex
