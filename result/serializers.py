from django.utils.timezone import now
from rest_framework import serializers
from services.constants import ResultChoices
from courses.models import StudentEnrollment,Course
from result.models import Result
from services.service import ResultCalculator
from accounts.serializers import *
from courses.serializers import CourseMiniSerializer


class ResultSerializer(serializers.ModelSerializer, ResultCalculator):
    student = UserMiniSerializer(read_only=True)
    course = CourseMiniSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_student=True), write_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model = Result
        fields = "__all__"
        read_only_fields = ['total_marks','grade','status']

    def validate(self, data):
        instance = self.instance
        student = data.get('student_id') or getattr(instance, 'student', None)
        course = data.get('course_id') or getattr(instance, 'course', None)

        if not course:
            raise serializers.ValidationError("Course is required")

        is_enrolled = StudentEnrollment.objects.filter(course=course,student=student).exists()

        if not is_enrolled:
            raise serializers.ValidationError("This student is not enrolled in the selected course.")

        if course.result_deadline and now().date() > course.result_deadline:
            raise serializers.ValidationError("The Deadline to publish result has been passed,you can't publish result.")

        data['total_marks'] = round(self.calculate_total_marks(course, instance, data),2)

        if data['total_marks'] >=85:
            data['grade'] = 'A'
            data['remarks']="Excellent"
            data['status'] = ResultChoices.PASS

        elif data['total_marks'] >=70:
            data['grade'] = 'B'
            data['remarks'] = "Good"
            data['status'] = ResultChoices.PASS

        elif data['total_marks'] >=50:
            data['grade'] = 'C'
            data['remarks'] = "Pass"
            data['status'] = ResultChoices.PASS

        else:
            data['grade'] = 'F'
            data['remarks'] = "Fail"
            data['status'] = ResultChoices.FAIL


        return data

    def create(self, validated_data):
        course = validated_data.pop('course_id')
        student = validated_data.pop('student_id')

        return Result.objects.create(course=course,student=student,**validated_data)


