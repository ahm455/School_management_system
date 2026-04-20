from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from accounts.serializers import UserMiniSerializer
from accounts.models import *


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserMiniSerializer(read_only=True)
    students = UserMiniSerializer(many=True, read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_teacher=True), write_only=True)

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

        total = mid + quiz + assign + final

        if round(total) != 100:
            raise ValidationError(f'Total weightage is {total}, must be 100')

        return data
    def create(self, validated_data):
        teacher = validated_data.pop('teacher_id')
        return Course.objects.create(teacher=teacher,**validated_data)


class CourseMiniSerializer(serializers.ModelSerializer):
    teacher = UserMiniSerializer(read_only=True)


    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher']


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student = UserMiniSerializer(read_only=True)
    course = CourseMiniSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_student=True), write_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),write_only=True)

    class Meta:
        model = StudentEnrollment
        fields = '__all__'

    def validate(self, data):
        course = data.get('course_id')
        student = data.get('student_id')
        semester = student.student.semester

        if course.semester != semester:
            raise ValidationError(
                f"Student must belong to semester {course.semester}")

        return data

    def create(self, validated_data):
        course = validated_data.pop('course_id')
        student = validated_data.pop('student_id')
        return StudentEnrollment.objects.create(course=course, student=student, **validated_data)


class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseMiniSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),write_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['created_by']
    def create(self, validated_data):
        course = validated_data.pop('course_id')
        return Assignment.objects.create(course=course, **validated_data)


class SubmissionSerializer(serializers.ModelSerializer):
    student = UserMiniSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)
    assignment_id = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all(),write_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'status']

    def create(self, validated_data):
        assignment = validated_data.pop('assignment_id')
        return Submission.objects.create(assignment=assignment, **validated_data)



class GradingAssignmentSerializer(serializers.ModelSerializer):
    student = UserMiniSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'assignment', 'file']

    def validate(self, data):
        instance = self.instance
        user = self.context['request'].user

        if user.is_teacher:
            if instance.assignment.course.teacher != user:
                raise ValidationError("Only assigned teacher can mark.")

        return data

class CourseAnalyticsSerializer(serializers.Serializer):
    course = CourseMiniSerializer()
    average_marks = serializers.FloatField(allow_null=True)
    top_performer = UserMiniSerializer(allow_null=True)
    top_score = serializers.FloatField(allow_null=True)
    pass_count = serializers.IntegerField()
    fail_count = serializers.IntegerField()
    total_students = serializers.IntegerField()