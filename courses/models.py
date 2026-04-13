from django.db import models
from accounts.common import CreateUpdateTime
from accounts.models import User
from accounts.constants import SemesterChoices,StatusChoices,RolesChoices


class Course(CreateUpdateTime):
    name = models.CharField()
    code = models.CharField()
    Semester=models.CharField(max_length=10,choices=SemesterChoices,null=True)
    midterm_weightage=models.FloatField(null=True)
    quiz_weightage=models.FloatField(null=True)
    assignment_weight=models.FloatField(null=True)
    finalterm_weightage=models.FloatField(null=True)

    class Meta:
        unique_together = ('name','code')

    def __str__(self):
        return f"{self.name}"


class Enrollment(CreateUpdateTime):
    student = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.STUDENT},related_name='student_enrollment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='enrollments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.TEACHER},related_name='teacher_enrollment')

    class Meta:
        unique_together = ('student','course')

    def __str__(self):
        return f"{self.teacher} {self.course}"

class Assignment(CreateUpdateTime):
    name=models.CharField()
    description = models.TextField()
    status=models.CharField(choices=StatusChoices,max_length=10,null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.STUDENT},related_name='assign_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='assignment')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.TEACHER},related_name='assign_teacher')
    deadline = models.DateField()

    class Meta:
        unique_together = ('student','course','name')

    def __str__(self):
        return f"{self.student}({self.course}): {self.status}"