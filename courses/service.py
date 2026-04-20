from django.db.models import Avg, Count, Q
from result.models import Result
from services.constants import ResultChoices
from courses.models import Course, Assignment
from notification.service import create_notification

def get_course_analytics(course_id):
    results = Result.objects.filter(course_id=course_id)
    course = Course.objects.get(id=course_id)
    average_marks = results.aggregate(avg=Avg("total_marks"))["avg"]
    top = results.order_by("-total_marks").select_related("student").first()
    pass_count = results.filter(status=ResultChoices.PASS).count()
    fail_count = results.filter(status=ResultChoices.FAIL).count()

    return {
        "course_id": course_id,
        "course_name":course.name,
        "course_teacher": course.teacher.full_name,
        "average_marks": average_marks,
        "top_performer": top.student.full_name if top else None,
        "top_score": top.total_marks if top else None,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "total_students": results.count(),
    }

def grade_submission(submission):
    submission.graded=True
    submission.save()

    if submission.graded:
        create_notification(
            user=submission.student,title=f"Assignment Graded {submission.assignment.course.name}",
            message=f"Your assignment has been graded .You got {submission.marks}",type="Assignment")