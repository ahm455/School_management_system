from typing import cast
from django.utils.timezone import now
from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User


class ResultPermission(BasePermission):

    def has_permission(self, request, view):
        user = cast(User, request.user)

        if not user or not user.is_authenticated:
            return False

        if request.method not in SAFE_METHODS:
            return user.is_teacher

        return True

    def has_object_permission(self, request, view, obj):
        user = cast(User, request.user)
        course = obj.course

        if user.is_student:
            return obj.student == user and request.method in SAFE_METHODS

        if user.is_headmaster:
            return request.method in SAFE_METHODS

        if user.is_teacher:
            if course.teacher != user:
                return False

            if course.result_deadline and now() > course.result_deadline:
                return request.method in SAFE_METHODS

            return True

        return False