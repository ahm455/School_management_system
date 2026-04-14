from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from courses.models import *
from courses.serializers import *
from .permissions import CourseHeadmasterPermission, EnrollmentPermission, AssignmentSubmissionPermission
from accounts.constants import RolesChoices


def get_role(user):
    return getattr(user, 'role', None)


class CourseCreateList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CourseHeadmasterPermission]

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Course.objects.filter(enrollments__student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Course.objects.filter(teachers__teacher=user).distinct()
        return Course.objects.all()

    def perform_create(self, serializer):
        if get_role(self.request.user) != RolesChoices.HEADMASTER:
            raise PermissionDenied("Only Headmaster can create courses")
        serializer.save()


class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CourseHeadmasterPermission]
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Course.objects.filter(enrollments__student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Course.objects.filter(teachers__teacher=user).distinct()
        return Course.objects.all()



class CourseTeacherCreateList(generics.ListCreateAPIView):
    serializer_class = CourseTeacherSerializer
    permission_classes = [CourseHeadmasterPermission]

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.TEACHER:
            return CourseTeacher.objects.filter(teacher=user).distinct()
        return CourseTeacher.objects.all()

    def perform_create(self, serializer):
        if get_role(self.request.user) != RolesChoices.HEADMASTER:
            raise PermissionDenied("Only Headmaster can assign teachers")
        serializer.save()


class CourseTeacherRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseTeacherSerializer
    permission_classes = [CourseHeadmasterPermission]
    lookup_url_kwarg = 'course_teacher_id'

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.TEACHER:
            return CourseTeacher.objects.filter(teacher=user).distinct()
        return CourseTeacher.objects.all()



class EnrollmentCreateList(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [EnrollmentPermission]

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Enrollment.objects.filter(student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Enrollment.objects.filter(course__teachers__teacher=user).distinct()
        return Enrollment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            serializer.save(student=user)
        else:
            serializer.save()


class EnrollmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [EnrollmentPermission]
    lookup_url_kwarg = 'enrollment_id'

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Enrollment.objects.filter(student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Enrollment.objects.filter(course__teachers__teacher=user).distinct()
        return Enrollment.objects.all()




class AssignmentCreateList(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentSubmissionPermission]

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Assignment.objects.filter(course__enrollments__student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Assignment.objects.filter(course__teachers__teacher=user).distinct()
        return Assignment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != RolesChoices.TEACHER:
            raise PermissionDenied("Only teachers can create assignments")

        course = serializer.validated_data.get("course")

        if not course.teachers.filter(teacher=user).exists():
            raise PermissionDenied("You are not assigned to this course")

        serializer.save()


class AssignmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentSubmissionPermission]
    lookup_url_kwarg = 'assignment_id'

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Assignment.objects.filter(course__enrollments__student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Assignment.objects.filter(course__teachers__teacher=user).distinct()
        return Assignment.objects.all()



class SubmissionCreateList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [AssignmentSubmissionPermission]

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Submission.objects.filter(student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Submission.objects.filter(assignment__course__teachers__teacher=user).distinct()
        return Submission.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        role = get_role(user)

        if role != RolesChoices.STUDENT:
            raise PermissionDenied("Only students can submit assignments")

        assignment = serializer.validated_data.get("assignment")

        if not assignment.course.enrollments.filter(student=user).exists():
            raise PermissionDenied("You are not enrolled in this course")

        serializer.save(student=user,status=StatusChoices.SUBMITTED)


class SubmissionRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [AssignmentSubmissionPermission]
    lookup_url_kwarg = 'submission_id'

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)

        if role == RolesChoices.STUDENT:
            return Submission.objects.filter(student=user).distinct()
        elif role == RolesChoices.TEACHER:
            return Submission.objects.filter(assignment__course__teachers__teacher=user).distinct()
        return Submission.objects.all()

    def perform_destroy(self, instance):
        instance = self.get_object()
        user = self.request.user
        role= get_role(user)

        if role != RolesChoices.TEACHER:
            raise PermissionDenied("Only teachers can delete submissions")

        if not instance.assignment.course.teachers.filter(teacher=user).exists():
            raise PermissionDenied("Not your course")

        instance.delete()
