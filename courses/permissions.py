from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.constants import RolesChoices
from accounts.models import User
from typing import cast


class CourseHeadmasterPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = cast(User, request.user)

        if request.method in SAFE_METHODS:
            return True

        return user.is_headmaster



class EnrollmentPermission(BasePermission):

    def has_permission(self, request, view):
        user = cast(User, request.user)
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == "POST":
            return user.is_student

        return True

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True


        return obj.student == request.user

class AssignmentSubmissionPermission(BasePermission):

    def has_permission(self, request, view):
        user = cast(User, request.user)

        if not user or not user.is_authenticated:
            return False

        if user.is_headmaster:
            return request.method in SAFE_METHODS

        if user.is_student:
            name = view.__class__.__name__.lower()
            if "submission" in name:
                return request.method in ["GET", "POST"]
            if "assignment" in name:
                return request.method in SAFE_METHODS

        if user.is_teacher:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = cast(User, request.user)

        if user.is_headmaster:
            return request.method in SAFE_METHODS

        if user.is_student:
            if request.method not in SAFE_METHODS:
                return False

            if hasattr(obj, "student"):
                return obj.student == user

            if hasattr(obj, "course"):
                return obj.course.enrollments.filter(student=user).exists()

            return False

        if user.is_teacher:
            if hasattr(obj, "course"):
                return obj.course.teachers.filter(teacher=user).exists()

            if hasattr(obj, "assignment"):
                return obj.assignment.course.teachers.filter(teacher=user).exists()

            return False

        return False
