from rest_framework import serializers
from attendance.models import Attendance
from accounts.serializers import *
from courses.serializers import CourseMiniSerializer
from courses.serializers import Course


class AttendanceSerializer(serializers.ModelSerializer):
    student=UserMiniSerializer(read_only=True)
    course=CourseMiniSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_student=True), write_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course', write_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

    def validate(self, data):
        instance = self.instance
        request = self.context.get("request")
        user = request.user
        course = data.get('course') or getattr(instance, 'course', None)

        if course.teacher != user:
            raise serializers.ValidationError("You are not assigned to this course.")

        return data

    def create(self, validated_data):
        user = validated_data.pop("student_id")
        validated_data["student"] = user
        return super().create(validated_data)
