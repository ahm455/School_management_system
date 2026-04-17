from typing import cast
from rest_framework.permissions import BasePermission
from accounts.models import User


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = cast(User, request.user)
        return user.is_authenticated and user.is_student


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        user = cast(User, request.user)
        return user.is_authenticated and user.is_teacher


class IsHeadmaster(BasePermission):
    def has_permission(self, request, view):
        user = cast(User, request.user)
        return user.is_authenticated and user.is_headmaster