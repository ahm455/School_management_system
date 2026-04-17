from accounts.models import User
from services.common import CreateUpdateTime
from courses.models import Course
from services.constants import *

class Attendance(CreateUpdateTime):
    date = models.DateField(auto_now_add=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='attendance')
    student = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_student': True},related_name='student_attendance')
    status = models.CharField(max_length=10, choices=AttentanceChoices, default=AttentanceChoices.PRESENT)

    class Meta:
        unique_together = [['date', 'course','student']]

    def __str__(self):
        return f'{self.date} | {self.course} | {self.student}'