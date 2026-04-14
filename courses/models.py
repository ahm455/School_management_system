from django.db import models
from accounts.common import CreateUpdateTime
from accounts.models import User
from accounts.constants import SemesterChoices, StatusChoices, RolesChoices


class Course(CreateUpdateTime):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    semester = models.CharField(max_length=10, choices=SemesterChoices, null=True, blank=True)
    teacher=models.ManyToManyField(User,through='CourseTeacher',related_name='coursesteachers')
    student_enrolled=models.ManyToManyField(User,through='Enrollment',related_name='enrollment_courses')
    midterm_weightage = models.FloatField(default=0)
    quiz_weightage = models.FloatField(default=0)
    assignment_weightage = models.FloatField(default=0)
    finalterm_weightage = models.FloatField(default=0)
    result_deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [['name','code','semester']]

    def __str__(self):
        return f"{self.name} ({self.code})"


class CourseTeacher(CreateUpdateTime):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.TEACHER},related_name='teacher_courses')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='teachers')

    class Meta:
        unique_together = [['teacher', 'course']]

    def __str__(self):
        return f"{self.teacher} - {self.course}"


class Enrollment(CreateUpdateTime):
    student = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.STUDENT},related_name='enrollments')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollments')

    class Meta:
        unique_together = [['student','course']]

    def __str__(self):
        return f"{self.student} - {self.course}"


class Assignment(CreateUpdateTime):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='assignments')
    deadline = models.DateField()

    class Meta:
        unique_together = [['name', 'course']]

    def __str__(self):
        return f"{self.name} - {self.course}"


class Submission(CreateUpdateTime):
    student = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role': RolesChoices.STUDENT},related_name='submissions')
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name='submissions')
    file=models.FileField(upload_to='submissions/')
    status = models.CharField(choices=StatusChoices, max_length=10,default=StatusChoices.PENDING)

    class Meta:
        unique_together = [['student','assignment']]

    def __str__(self):
        return f"{self.student} - {self.assignment} - {self.status}"