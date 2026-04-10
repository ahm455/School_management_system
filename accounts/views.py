from django.shortcuts import render
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework import generics
from .permissions import *

class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AccountPermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.HEADMASTER:
            return User.objects.all()
        return User.objects.filter(id=user.id)



class UserRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    serializer_class = UserSerializer
    permission_classes = [AccountPermission]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == RolesChoices.HEADMASTER:
            return User.objects.all()
        return User.objects.filter(id=user.id)