from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.timezone import now
from accounts.constants import RolesChoices

class ResultPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)

        if request.method not in SAFE_METHODS:
            return role == RolesChoices.TEACHER

        return True


    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)

        if request.method in SAFE_METHODS:
            if role == RolesChoices.STUDENT:
                return obj.student == request.user
            if role == RolesChoices.TEACHER:
                return obj.teacher == request.user
            if role == RolesChoices.HEADMASTER:
                return True
            return False

        if role == RolesChoices.TEACHER:
            return (
                obj.teacher == request.user and
                (obj.deadline is None or obj.deadline >= now().date())
            )

        return False