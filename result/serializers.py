from rest_framework import serializers

from courses.models import Course
from result.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

    def validate(self, data):
        course = data.get('course')
        midterm = data.get('midterm_marks', 0)
        quiz = data.get('quiz_marks', 0)
        assignment = data.get('assignment_marks', 0)
        finalterm = data.get('finalterm_marks', 0)

        data['total_marks'] = (((midterm*course.midterm_weightage)/50)+((quiz*course.quiz_weightage)/20)+((assignment*course.assignment_weight)/20)+((finalterm*course.finalterm_weightage)/100))

        return data


