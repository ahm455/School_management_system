from django.db import models
from accounts.common import CreateUpdateTime
from courses.models import Course
from accounts.models import User
from courses.models import Course
from accounts.constants import ResultChoices , RolesChoices


class Result(CreateUpdateTime):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='result')
    student=models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.STUDENT},related_name='student_result')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.TEACHER},related_name='teacher_result')
    status=models.CharField(max_length=10,choices=ResultChoices,default=ResultChoices.FAIL)
    midterm_marks = models.FloatField(default=0)
    assignment_marks = models.FloatField(default=0)
    quiz_marks = models.FloatField(default=0)
    finalterm_marks = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    grade=models.CharField(max_length=5)
    remarks=models.TextField(null=True)
    deadline=models.DateField(null=True)

    class Meta:
        unique_together = [[ 'course','student']]


