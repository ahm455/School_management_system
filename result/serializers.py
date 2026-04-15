from rest_framework import serializers
from courses.models import Course
from result.models import Result
from .service import ResultCalculator


class ResultSerializer(serializers.ModelSerializer, ResultCalculator):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['total_marks']

    def validate(self, data):
        instance = self.instance
        course = data.get('course') or getattr(instance, 'course', None)

        if not course:
            raise serializers.ValidationError("Course is required")

        data['total_marks'] = round(self.calculate_total_marks(course, instance, data),2)

        return data