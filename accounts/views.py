from django.shortcuts import render
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework import generics

class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    serializer_class = UserSerializer