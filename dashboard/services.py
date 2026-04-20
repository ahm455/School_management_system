from result.models import Result
from courses.models import StudentEnrollment
from attendance.models import Attendance
from courses.models import Course
from accounts.models import User
from services.constants import AttentanceChoices,ResultChoices
from django.db.models import Avg, Count
from courses.models import Course, StudentEnrollment
from result.models import Result


def get_student_dashboard(user):
    enrollments = StudentEnrollment.objects.filter(student=user).select_related('course')

    data = []

    for enrollment in enrollments:
        course = enrollment.course
        result = Result.objects.filter(student=user, course=course).first()
        attendance_qs = Attendance.objects.filter(student=user, course=course)
        present_classes = attendance_qs.filter(status=AttentanceChoices.PRESENT).count()
        total_classes = attendance_qs.count()


        attendance_percentage = (
            (present_classes / total_classes) * 100 if total_classes > 0 else 0)

        data.append({
            "course_id": course.id,
            "course": course.name,
            "midterm marks": result.midterm_marks if result else None,
            "Quiz marks": result.quiz_marks if result else None,
            "Assignment marks": result.assignment_marks if result else None,
            "final marks": result.finalterm_marks if result else None,
            "total marks": result.total_marks if result else None,
            "grade": result.grade if result else None,
            "attendance_percentage": round(attendance_percentage, 2),
        })

    return data

def get_teacher_dashboard(user):
    user=User.objects.get(id=user.id)
    courses = Course.objects.filter(teacher=user).prefetch_related('course_enrollments','result')
    data = []

    for course in courses:
        total_students = course.course_enrollments.count()
        graded_students = course.result.filter(course=course).count()
        result_completion_percentage = graded_students / total_students*100

        data.append({
            "course_id": course.id,
            "course_name": course.name,
            "total_students": total_students,
            "graded_students": graded_students,
            "result_completion": f"{graded_students}/{total_students}",
            "result_completion_percentage": round(result_completion_percentage, 2),
        })

    return data


def get_headmaster_dashboard():
    courses = Course.objects.all().prefetch_related('result','course_enrollments').select_related('teacher')
    total_students = User.objects.filter(is_student=True).count()
    total_teachers = User.objects.filter(is_teacher=True).count()
    total_courses = courses.count()

    course_list = []

    for course in courses:
        results = course.result.all()
        total_students_course = course.course_enrollments.count()
        graded_students = results.values('student').distinct().count()

        if total_students_course > 0 and graded_students > 0:
            completion_percentage = (
                (graded_students / total_students_course) * 100)
        else:
            completion_percentage = 0

        avg_marks = results.aggregate(avg=Avg('total_marks'))['avg']
        top_result = results.order_by('-total_marks').select_related('student').first()
        total_students_count = course.course_enrollments.count()
        pass_count = results.filter(status=ResultChoices.PASS).count()
        fail_count = results.filter(status=ResultChoices.FAIL).count()

        course_list.append({
            "course_id": course.id,
            "course_name": course.name,
            "teacher_id": course.teacher.id,
            "teacher_name": course.teacher.full_name,
            "average_marks": avg_marks,
            "completion_percentage": round(completion_percentage, 2),
            "top_performer": { "student_id": top_result.student.id,
                               "student_name":top_result.student.full_name,
                                "marks": top_result.total_marks} if top_result else None,
            "total_students_count": total_students_count,
            "pass_count": pass_count,
            "fail_count": fail_count,

        })

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "courses": course_list
    }