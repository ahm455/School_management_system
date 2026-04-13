from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from result.models import Result
from result.serializers import ResultSerializer
from .permissions import ResultPermission
from accounts.constants import RolesChoices

class ResultCreateList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [ResultPermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Result.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Result.objects.filter(course__teachers__teacher=user).distinct()
        return Result.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != RolesChoices.TEACHER:
            raise PermissionDenied("Only teachers can create results")

        course = serializer.validated_data.get("course")

        if not course.teachers.filter(teacher=user).exists():
            raise PermissionDenied("Not your course")

        serializer.save()
class ResultRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    lookup_url_kwarg = 'result_id'
    permission_classes = [ResultPermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.STUDENT:
            return Result.objects.filter(student=user)
        elif role == RolesChoices.TEACHER:
            return Result.objects.filter(course__teachers__teacher=user).distinct()
        return Result.objects.all()