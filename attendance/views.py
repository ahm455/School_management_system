from django.shortcuts import render
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from rest_framework import generics

class AttendanceCreateList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    lookup_url_kwarg = 'Attendance_id'
    serializer_class = AttendanceSerializer