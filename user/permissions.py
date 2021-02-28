from rest_framework.permissions import BasePermission

from resources.models import Role
from user.models import UserRole


class IsActive(BasePermission):
    """
    Allows access only to "is_active" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_active


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(name="student")
        roles = UserRole.objects.filter(user=user, role=role)
        if not roles:
            return False
        else:
            return True
