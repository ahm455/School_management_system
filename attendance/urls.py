from django.urls import path
from .views import *

app_name = 'attendance'

urlpatterns = [
    path('', AttendanceCreateList.as_view(), name='customer_list_create'),
    path("<int:Attendance_id>/",AttendanceRetrieveUpdateDelete.as_view(), name='customer_detail'),
 ]
