from result.models import Result


class ResultCalculator:

    def calculate_total_marks(self, course, instance=None, data=None):
        instance = instance or Result()
        data = data or {}

        midterm = data.get('midterm_marks')
        if midterm is None:
            midterm = getattr(instance, 'midterm_marks', 0) or 0

        quiz = data.get('quiz_marks')
        if quiz is None:
            quiz = getattr(instance, 'quiz_marks', 0) or 0

        assignment = data.get('assignment_marks')
        if assignment is None:
            assignment = getattr(instance, 'assignment_marks', 0) or 0

        finalterm = data.get('finalterm_marks')
        if finalterm is None:
            finalterm = getattr(instance, 'finalterm_marks', 0) or 0

        total = (
            (midterm * course.midterm_weightage / 100) +
            (quiz * course.quiz_weightage / 100) +
            (assignment * course.assignment_weightage / 100) +
            (finalterm * course.finalterm_weightage / 100)
        )

        return total