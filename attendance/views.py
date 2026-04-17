from typing import cast
from rest_framework.exceptions import PermissionDenied
from accounts.models import User
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from rest_framework import generics

from services.constants import AttentanceChoices
from .permissions import AttendancePermission
from .services import mark_absent


class AttendanceCreateList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Attendance.objects.filter(student=user)

        if user.is_teacher:
            return Attendance.objects.filter(course__teacher=user)

        return Attendance.objects.all()

    def perform_create(self, serializer):
        user = cast(User, self.request.user)
        course = serializer.validated_data.get("course")
        student = serializer.validated_data.get("student")

        if course.teacher != user:
            raise PermissionDenied("Not your course")

        if not course.course_enrollments.filter(student=student).exists():
            raise PermissionDenied("Student not enrolled in this course")

        attendance = serializer.save()

        if attendance.status == AttentanceChoices.ABSENT:
            mark_absent(attendance)


class AttendanceRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    lookup_url_kwarg = 'Attendance_id'
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Attendance.objects.filter(student=user)

        if user.is_teacher:
            return Attendance.objects.filter(course__teacher=user)

        return Attendance.objects.all()