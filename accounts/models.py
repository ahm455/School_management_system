from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.common import CreateUpdateTime
from .constants import SemesterChoices


class User(CreateUpdateTime,AbstractUser):
    clerk_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    full_name=models.CharField(max_length=20)
    semester = models.IntegerField(choices=SemesterChoices,blank=True, null=True)
    email=models.EmailField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=11,unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_headmaster = models.BooleanField(default=False)
    date_of_birth=models.DateField(null=True)
    date_joined=models.DateField(null=True)

    def __str__(self):
        return f"{self.full_name}({self.date_joined})"


