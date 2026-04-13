from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.constants import RolesChoices
from courses.models import CourseTeacher
from datetime import date


class AttendancePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        role = getattr(user, 'role', None)

        if not user or not user.is_authenticated:
            return False

        if request.method == "POST":
            return role == RolesChoices.TEACHER

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = getattr(user, 'role', None)
        course = obj.course

        if role == RolesChoices.STUDENT:
            return obj.student == user and request.method in SAFE_METHODS

        if role == RolesChoices.HEADMASTER:
            return request.method in SAFE_METHODS

        if role == RolesChoices.TEACHER:
            is_teacher = CourseTeacher.objects.filter(teacher=user,course=course).exists()

            if not is_teacher:
                return False

            if obj.date != date.today():
                return request.method in SAFE_METHODS

            return True

        return False