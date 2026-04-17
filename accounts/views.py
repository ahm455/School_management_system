from typing import cast
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from accounts.models import *
from accounts.serializers import *
from dashboard.permissions import IsHeadmaster
from .permissions import AccountPermission


class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AccountPermission]

    def perform_create(self, serializer):
        user = cast(User, self.request.user)

        if not user.is_headmaster:
            raise PermissionDenied("Only headmaster can create users")

        serializer.save()

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_headmaster:
            return User.objects.all()

        return User.objects.filter(id=user.id)

class UserRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    serializer_class = UserSerializer
    permission_classes = [AccountPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_headmaster:
            return User.objects.all()

        return User.objects.filter(id=user.id)

class StudentUpdate(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AccountPermission]
    def get_queryset(self):
        user = cast(User, self.request.user)
        if user.is_headmaster:
            return Student.objects.all()
        return Student.objects.filter(id=user.id)

class TeacherUpdate(generics.RetrieveUpdateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AccountPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)
        if user.is_headmaster:
            return Teacher.objects.all()
        return Teacher.objects.filter(id=user.id)

class HeadmasterUpdate(generics.RetrieveUpdateAPIView):
    queryset = Headmaster.objects.all()
    serializer_class = HeadmasterSerializer
    permission_classes = [AccountPermission,IsHeadmaster]

