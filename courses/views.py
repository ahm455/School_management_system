from courses.models import *
from courses.serializers import *
from rest_framework import generics

class CourseCreateList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    lookup_url_kwarg = 'Course_id'
    serializer_class = CourseSerializer

class EnrollmentCreateList(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class EnrollmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    lookup_url_kwarg = 'Enrollment_id'
    serializer_class = EnrollmentSerializer

class AssignmentCreateList(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    lookup_url_kwarg = 'Assignment_id'
    serializer_class = AssignmentSerializer