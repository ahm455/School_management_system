from clerk_backend_api.models import totalcount
from django.utils.timezone import now
from rest_framework import serializers
from services.constants import ResultChoices
from courses.models import StudentEnrollment
from result.models import Result
from services.service import ResultCalculator


class ResultSerializer(serializers.ModelSerializer, ResultCalculator):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['total_marks','grade','status']

    def validate(self, data):
        instance = self.instance
        course = data.get('course') or getattr(instance, 'course', None)
        student = data.get('student') or getattr(instance, 'student', None)

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

