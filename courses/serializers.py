from rest_framework import serializers
from .models import  *
from django.core.exceptions import ValidationError

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        mid = data.get('midterm_weightage', 0)
        quiz = data.get('quiz_weightage', 0)
        assign = data.get('assignment_weight', 0)
        final = data.get('finalterm_weightage', 0)

        total_weightage = mid + quiz + assign + final

        if total_weightage != 100:
            raise ValidationError(f'Total weightage is {total_weightage}, must be 100')

        return data

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        course = data.get('course')
        student = data.get('student')

        if course is None or student is None:
            raise ValidationError("Both 'course' and 'student' must be provided.")

        if course.Semester != student.semester:
            raise ValidationError(f'Student must belong to semester {course.Semester} to enroll.')

        return data


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'



