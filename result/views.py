from django.shortcuts import render
from result.models import Result
from result.serializers import ResultSerializer
from rest_framework import generics

class ResultCreateList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class ResultRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    lookup_url_kwarg = 'result_id'
    serializer_class = ResultSerializer