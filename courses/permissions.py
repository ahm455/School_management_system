from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.constants import RolesChoices

class CoursePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, 'role', None) == RolesChoices.HEADMASTER

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)

        if role == RolesChoices.STUDENT:
            return obj.enrollments.filter(student=request.user).exists()


        if role == RolesChoices.TEACHER:
            return obj.enrollments.filter(teacher=request.user).exists()

        return True