from rest_framework import generics
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
            return Result.objects.filter(teacher=user)
        return Result.objects.all()

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
            return Result.objects.filter(teacher=user)
        return Result.objects.all()