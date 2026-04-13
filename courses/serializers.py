from rest_framework import serializers
from .models import  *
from rest_framework.exceptions import ValidationError

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


    def validate(self, data):
        instance = self.instance

        if instance:
            mid = data.get('midterm_weightage', instance.midterm_weightage)
            quiz = data.get('quiz_weightage', instance.quiz_weightage)
            assign = data.get('assignment_weightage', instance.assignment_weightage)
            final = data.get('finalterm_weightage', instance.finalterm_weightage)
        else:
            mid = data.get('midterm_weightage', 0)
            quiz = data.get('quiz_weightage', 0)
            assign = data.get('assignment_weightage', 0)
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
        instance = self.instance

        course = data.get('course', getattr(instance, 'course', None))
        student = data.get('student', getattr(instance, 'student', None))

        if course is None or student is None:
            raise ValidationError("Both 'course' and 'student' must be provided.")

        if course.semester != student.semester:
            raise ValidationError(f'Student must belong to semester {course.semester} to enroll.')

        return data


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class CourseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTeacher
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student','status']

