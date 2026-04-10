import requests
from rest_framework import generics
from courses.models import *
from courses.serializers import *
from .permissions import CoursePermission
from accounts.constants import RolesChoices
from rest_framework.exceptions import PermissionDenied

class CourseCreateList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CoursePermission]

    def perform_create(self, serializer):
        role = getattr(self.request.user, 'role', None)
        if role != RolesChoices.HEADMASTER:
            raise PermissionDenied("Only Headmaster can create courses")
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Course.objects.filter(enrollments__student=user)
        elif role == RolesChoices.TEACHER:
            return Course.objects.filter(enrollments__teacher=user)
        return Course.objects.all()

class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'Course_id'
    permission_classes = [CoursePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Course.objects.filter(enrollments__student=user)
        elif role == RolesChoices.TEACHER:
            return Course.objects.filter(enrollments__teacher=user)
        return Course.objects.all()

class EnrollmentCreateList(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [CoursePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Enrollment.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Enrollment.objects.filter(teacher=user)
        return Enrollment.objects.all()

class EnrollmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    lookup_url_kwarg = 'Enrollment_id'
    permission_classes = [CoursePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Enrollment.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Enrollment.objects.filter(teacher=user)
        return Enrollment.objects.all()

class AssignmentCreateList(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [CoursePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Assignment.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Assignment.objects.filter(teacher=user)
        return Assignment.objects.all()

class AssignmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_url_kwarg = 'Assignment_id'
    permission_classes = [CoursePermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Assignment.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Assignment.objects.filter(teacher=user)
        return Assignment.objects.all()





