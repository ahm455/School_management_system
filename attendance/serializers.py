from rest_framework import serializers
from attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
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