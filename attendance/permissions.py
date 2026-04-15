from typing import cast
from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
from datetime import date


class AttendancePermission(BasePermission):

    def has_permission(self, request, view):
        user = cast(User, request.user)

        if not user or not user.is_authenticated:
            return False

        if request.method not in SAFE_METHODS:
            return user.is_teacher

        if user.is_student:
            return request.method in SAFE_METHODS

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

            if obj.date != date.today():
                return request.method in SAFE_METHODS

            return True

        return False