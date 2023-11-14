from django.db import models

import uuid

from django.contrib.auth.models import AbstractUser
from core.models import SoftDeleteModel


from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser, SoftDeleteModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # Admin related fields.
    # These fields will be used by the emergency services staff.
    is_admin = models.BooleanField(default=False)
    admin_category = models.ForeignKey(
        "reports.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phone"],
                condition=models.Q(phone__isnull=False),
                name="nullable_phone_unique",
            )
        ]

    def __str__(self):
        return self.email

    @property
    def auth_tokens(self):
        """
        Create authentication tokens for user.
        """
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
