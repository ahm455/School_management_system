from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.constants import RolesChoices


class CoursePermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role = request.user.role

        if request.method in SAFE_METHODS:
            return True

        return role == RolesChoices.HEADMASTER



class EnrollmentPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == "POST":
            return request.user.role == RolesChoices.STUDENT

        return True

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True


        return obj.student == request.user

class AssignmentSubmissionPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        role = getattr(user, 'role', None)

        if role == RolesChoices.HEADMASTER:
            return request.method in SAFE_METHODS

        if role == RolesChoices.STUDENT:
            name = view.__class__.__name__.lower()
            if "submission" in name:
                return request.method in ["GET", "POST"]
            if "assignment" in name:
                return request.method in SAFE_METHODS

        if role == RolesChoices.TEACHER:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = getattr(user, 'role', None)

        if role == RolesChoices.HEADMASTER:
            return request.method in SAFE_METHODS

        if role == RolesChoices.STUDENT:
            if request.method not in SAFE_METHODS:
                return False

            if hasattr(obj, "student"):
                return obj.student == user

            if hasattr(obj, "course"):
                return obj.course.enrollments.filter(student=user).exists()

            return False

        if role == RolesChoices.TEACHER:
            if hasattr(obj, "course"):
                return obj.course.teachers.filter(teacher=user).exists()

            if hasattr(obj, "assignment"):
                return obj.assignment.course.teachers.filter(teacher=user).exists()

            return False

        return False
