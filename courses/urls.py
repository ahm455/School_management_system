from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    path('', CourseCreateList.as_view(), name='Course_list_create'),
    path("<int:Course_id>/",CourseRetrieveUpdateDelete.as_view(), name='Course_detail'),
    path('enrollment/', EnrollmentCreateList.as_view(), name='Enrollment_list_create'),
    path("enrollment/<int:Enrollment_id>/",EnrollmentRetrieveUpdateDelete.as_view(), name='Enrollment_detail'),
    path('assignment/', AssignmentCreateList.as_view(), name='Assignment_list_create'),
    path("assignment/<int:Assignment_id>/",AssignmentRetrieveUpdateDelete.as_view(), name='Assignment_detail'),

 ]
