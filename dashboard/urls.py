from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('student', StudentDashboard.as_view()),
    path("teacher",TeacherDashboard.as_view()),
    path("headmaster",HeadmasterDashboard.as_view()),
]

