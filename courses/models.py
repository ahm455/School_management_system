from django.db import models
from services.common import CreateUpdateTime
from accounts.models import User
from services.constants import SemesterChoices, StatusChoices


class Course(CreateUpdateTime):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    semester = models.CharField(choices=SemesterChoices,blank=True, null=True)
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_teacher': True},related_name='teacher_courses')
    students = models.ManyToManyField(User,through='StudentEnrollment',related_name='enrollment_courses')
    midterm_weightage = models.FloatField(default=0)
    quiz_weightage = models.FloatField(default=0)
    assignment_weightage = models.FloatField(default=0)
    finalterm_weightage = models.FloatField(default=0)
    result_deadline = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = [['name', 'code', 'semester']]

    def __str__(self):
        return f"{self.name} ({self.code})"


class StudentEnrollment(CreateUpdateTime):
    student = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_student': True},related_name='student_enrollments')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='course_enrollments')

    class Meta:
        unique_together = [['student', 'course']]

    def __str__(self):
        return f"{self.student} - {self.course}"


class Assignment(CreateUpdateTime):
    name = models.CharField(max_length=50)
    description = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='assignments')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_teacher': True},related_name='Assignment_created_by')
    deadline = models.DateField()

    class Meta:
        unique_together = [['name', 'course']]

    def __str__(self):
        return f"{self.name} - {self.course}"


class Submission(CreateUpdateTime):
    student = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_student': True},related_name='submissions')
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    status = models.CharField(choices=StatusChoices,max_length=10,default=StatusChoices.PENDING)
    marks= models.IntegerField(default=0)
    graded= models.BooleanField(default=False)

    class Meta:
        unique_together = [['student', 'assignment']]

    def __str__(self):
        return f"{self.student} - {self.assignment} - {self.status}"