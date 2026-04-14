from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.common import CreateUpdateTime
from .constants import EducationChoices,SemesterChoices,RolesChoices


class User(CreateUpdateTime,AbstractUser):
    clerk_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    full_name=models.CharField(max_length=20)
    semester = models.CharField(max_length=10,choices=SemesterChoices,blank=True, null=True)
    email=models.EmailField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=11,unique=True)
    role=models.CharField(choices=RolesChoices,max_length=10,default=RolesChoices.STUDENT)
    date_of_birth=models.DateField(null=True)
    date_joined=models.DateField(null=True)

    def __str__(self):
        return f"{self.full_name}({self.date_joined})"

    @property
    def is_student(self):
        return self.role == RolesChoices.STUDENT

    @property
    def is_teacher(self):
        return self.role == RolesChoices.TEACHER

    @property
    def is_headmaster(self):
        return self.role == RolesChoices.HEADMASTER

