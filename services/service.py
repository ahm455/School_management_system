class ResultCalculator:

    def calculate_total_marks(self, course, instance=None, data=None):
        data = data

        mid_marks = data.get('midterm_marks')
        if mid_marks is None:
            mid_marks = getattr(instance, 'midterm_marks', 0) or 0

        quiz_mark = data.get('quiz_marks')
        if quiz_mark is None:
            quiz_mark = getattr(instance, 'quiz_marks', 0) or 0

        assignment_mark = data.get('assignment_marks')
        if assignment_mark is None:
            assignment_mark = getattr(instance, 'assignment_marks', 0) or 0

        final_marks = data.get('finalterm_marks')
        if final_marks is None:
            final_marks = getattr(instance, 'finalterm_marks', 0) or 0

        total = ((mid_marks * course.midterm_weightage / 50) +
                (quiz_mark * course.quiz_weightage / 20) +
                (assignment_mark * course.assignment_weightage / 20) +
                (final_marks * course.finalterm_weightage / 100))

        return total


from django.db.models import Avg, Max, Count, Q
from services.constants import ResultChoices

def get_course_analytics(course):
    results = course.result.all()

    return {
        "average_marks": results.aggregate(avg=Avg("total_marks"))["avg"],
        "top_performer": results.order_by("-total_marks").first(),
        "pass_count": results.filter(status=ResultChoices.PASS).count(),
        "fail_count": results.filter(status=ResultChoices.FAIL).count(),
        "total_students": results.count()
    }
