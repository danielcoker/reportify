from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = [
            "-created_at",
        ]


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        """
        Soft delete objects.
        """
        return super(SoftDeleteQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        """
        Hard delete objects.
        """
        return super(SoftDeleteQuerySet, self).delete()

    def alive(self):
        """
        Returns only non-deleted objects.
        """
        return self.filter(deleted_at=None)

    def dead(self):
        """
        Returns only deleted objects.
        """
        return self.exclude(deleted_at=None)


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(deleted_at=None)
        return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """
        Soft delete object.
        """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """
        Hard delete object.
        """
        super(SoftDeleteModel, self).delete()
