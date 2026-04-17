from django.db import models
from services.common import CreateUpdateTime
from accounts.models import User
from courses.models import Course
from services.constants import ResultChoices


class Result(CreateUpdateTime):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='result')
    student=models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_student':True},related_name='student_result')
    status=models.CharField(max_length=10,choices=ResultChoices,default=ResultChoices.FAIL)
    midterm_marks = models.FloatField(default=0)
    assignment_marks = models.FloatField(default=0)
    quiz_marks = models.FloatField(default=0)
    finalterm_marks = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    grade=models.CharField(max_length=5,blank=True)
    is_published=models.BooleanField(default=False)
    remarks=models.TextField(null=True)

    class Meta:
        unique_together = [[ 'course','student']]


