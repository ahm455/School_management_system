from rest_framework import serializers

from courses.models import Course
from result.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['total_marks']

    def calculate_total_marks(self, course, instance, data):
        instance = instance or Result()

        midterm = data.get('midterm_marks', getattr(instance, 'midterm_marks', 0))
        quiz = data.get('quiz_marks', getattr(instance, 'quiz_marks', 0))
        assignment = data.get('assignment_marks', getattr(instance, 'assignment_marks', 0))
        finalterm = data.get('finalterm_marks', getattr(instance, 'finalterm_marks', 0))

        return (
            (midterm * course.midterm_weightage / 100) +
            (quiz * course.quiz_weightage / 100) +
            (assignment * course.assignment_weightage / 100) +
            (finalterm * course.finalterm_weightage / 100)
        )

    def validate(self, data):
        instance = self.instance
        course = data.get('course') or getattr(instance, 'course')
        if not course:
            raise serializers.ValidationError("Course is required")

        data['total_marks'] = round(self.calculate_total_marks(course, instance, data),2)

        return data