from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import *
from .permissions import IsStudent, IsTeacher, IsHeadmaster


class StudentDashboard(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def list(self, request, *args, **kwargs):
        data = get_student_dashboard(request.user)
        return Response(data)

class TeacherDashboard(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request, *args, **kwargs):
        data = get_teacher_dashboard(request.user)
        return Response(data)

class HeadmasterDashboard(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsHeadmaster]

    def list(self, request, *args, **kwargs):
        data = get_headmaster_dashboard()
        return Response(data)





