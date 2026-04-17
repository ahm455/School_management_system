from django.contrib.auth.models import AbstractUser
from django.db import models
from services.common import CreateUpdateTime
from services.constants import SemesterChoices


class User(CreateUpdateTime,AbstractUser):
    clerk_id = models.CharField(max_length=255, unique=True, blank=True,null=True)
    full_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=11,unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_headmaster = models.BooleanField(default=False)
    date_of_birth=models.DateField(null=True)
    date_joined=models.DateField(null=True)

    def __str__(self):
        return f"{self.full_name}({self.date_joined})"

class Student(CreateUpdateTime):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='student')
    semester = models.CharField(choices=SemesterChoices,max_length=20,null=True,blank=True)

    def __str__(self):
        return self.user.full_name

class Teacher(CreateUpdateTime):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='teacher')
    salary=models.IntegerField(default=0)
    education=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.user.full_name

class Headmaster(CreateUpdateTime):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='headmaster')

    def __str__(self):
        return self.user.full_name
