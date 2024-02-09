import uuid

from django.db import models

from core.models import SoftDeleteModel, TimestampedModel
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Report(TimestampedModel, SoftDeleteModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In-Progress"
        RESOLVED = "resolved", "Resolved"

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
    longitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.id.hex
