from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    def has_permission(self, request, view):
        allowed_roles = getattr(view, 'allowed_roles', [])
        if not request.user.is_authenticated:
            return False
        return request.user.role in allowed_roles
