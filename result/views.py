from typing import cast
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from accounts.models import User
from result.models import Result
from result.serializers import ResultSerializer
from .permissions import ResultPermission


class ResultCreateList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [ResultPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Result.objects.filter(student=user)

        if user.is_teacher:
            return Result.objects.filter(course__teacher=user)

        return Result.objects.all()

    def perform_create(self, serializer):
        user = cast(User, self.request.user)

        if not user.is_teacher:
            raise PermissionDenied("Only teachers can create results")

        course = serializer.validated_data.get("course")

        if course.teacher != user:
            raise PermissionDenied("Not your course")

        serializer.save()


class ResultRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    lookup_url_kwarg = 'result_id'
    permission_classes = [ResultPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Result.objects.filter(student=user)

        if user.is_teacher:
            return Result.objects.filter(course__teacher=user)

        return Result.objects.all()