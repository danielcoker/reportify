from rest_framework import permissions


class IsEmergencyServiceAdmin(permissions.BasePermission):
    """
    Check if a user is an emergency service admin.
    """

    def has_permission(self, request, view):
        return request.user.is_admin
