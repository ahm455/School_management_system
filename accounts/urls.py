from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', UserCreateList.as_view(), name='account_list_create'),
    path("<int:user_id>/",UserRetrieveUpdateDelete.as_view(), name='account_detail'),
 ]
