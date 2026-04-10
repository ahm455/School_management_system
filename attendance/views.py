from django.shortcuts import render

from accounts.permissions import AccountPermission
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
            return Attendance.objects.filter(teacher=user)
        return Attendance.objects.all()

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
            return Attendance.objects.filter(teacher=user)
        return Attendance.objects.all()