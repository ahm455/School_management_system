from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.constants import RolesChoices

class AccountPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)

        if role == RolesChoices.HEADMASTER:
            return True

        if request.method == "DELETE":
            return False

        return obj == request.user