from typing import cast
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from accounts.models import User
from accounts.serializers import UserSerializer
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