
from rest_framework.exceptions import PermissionDenied

from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from rest_framework import generics
from accounts.constants import RolesChoices
from .permissions import AttendancePermission

class AttendanceCreateList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Attendance.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Attendance.objects.filter(course__teachers__teacher=user).distinct()
        return Attendance.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data.get("course")
        student = serializer.validated_data.get("student")

        if not course.teachers.filter(teacher=user).exists():
            raise PermissionDenied("Not your course")

        if not course.enrollments.filter(student=student).exists():
            raise PermissionDenied("Student not enrolled in this course")

        serializer.save()
class AttendanceRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    lookup_url_kwarg = 'Attendance_id'
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Attendance.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Attendance.objects.filter(course__teachers__teacher=user).distinct()
        return Attendance.objects.all()