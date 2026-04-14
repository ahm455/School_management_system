from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    path('', CourseCreateList.as_view(), name='Course_list_create'),
    path('<int:course_id>/', CourseRetrieveUpdateDelete.as_view(), name='Course_detail'),
    path('course-teacher/', CourseTeacherCreateList.as_view(), name='CourseTeacher_list_create'),
    path('course-teacher/<int:course_teacher_id>/', CourseTeacherRetrieveUpdateDelete.as_view(), name='CourseTeacher_detail'),
    path('enrollment/', EnrollmentCreateList.as_view(), name='Enrollment_list_create'),
    path('enrollment/<int:enrollment_id>/', EnrollmentRetrieveUpdateDelete.as_view(), name='Enrollment_detail'),
    path('assignment/', AssignmentCreateList.as_view(), name='Assignment_list_create'),
    path('assignment/<int:assignment_id>/', AssignmentRetrieveUpdateDelete.as_view(), name='Assignment_detail'),
    path('submission/', SubmissionCreateList.as_view(), name='Submission_list_create'),
    path('submission/<int:submission_id>/', SubmissionRetrieveUpdateDelete.as_view(), name='Submission_detail'),
]