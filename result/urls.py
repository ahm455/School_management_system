from django.urls import path
from .views import *

app_name = 'result'

urlpatterns = [
    path('', ResultCreateList.as_view(), name='result_list_create'),
    path("<int:result_id>/",ResultRetrieveUpdateDelete.as_view(), name='result_detail'),
 ]
