from typing import cast
from rest_framework.permissions import BasePermission
from accounts.models import User

class AccountPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = cast(User, request.user)

        if not user or not user.is_authenticated:
            return False

        if user.is_headmaster:
            return True

        if request.method == "DELETE":
            return False

        return obj == user