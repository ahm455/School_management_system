from typing import cast
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from accounts.models import User
from courses.models import *
from courses.serializers import *
from .permissions import CourseHeadmasterPermission, EnrollmentPermission, AssignmentSubmissionPermission
from accounts.constants import StatusChoices


class CourseCreateList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CourseHeadmasterPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Course.objects.filter(enrollments__student=user).distinct()

        if user.is_teacher:
            return Course.objects.filter(teacher=user)

        return Course.objects.all()

    def perform_create(self, serializer):
        user = cast(User, self.request.user)
        if not user.is_headmaster:
            raise PermissionDenied("Only Headmaster can create courses")
        serializer.save()


class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CourseHeadmasterPermission]
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Course.objects.filter(enrollments__student=user).distinct()

        if user.is_teacher:
            return Course.objects.filter(teacher=user)

        return Course.objects.all()


class StudentEnrollmentCreateList(generics.ListCreateAPIView):
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [EnrollmentPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return StudentEnrollment.objects.filter(student=user)

        if user.is_teacher:
            return StudentEnrollment.objects.filter(course__teacher=user)

        return StudentEnrollment.objects.all()

    def perform_create(self, serializer):
        user = cast(User, self.request.user)

        if user.is_student:
            serializer.save(student=user)
            return

        if user.is_teacher:
            course = serializer.validated_data.get("course")
            if course.teacher != user:
                raise PermissionDenied("Not your course")

        serializer.save()


class StudentEnrollmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [EnrollmentPermission]
    lookup_url_kwarg = 'enrollment_id'

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return StudentEnrollment.objects.filter(student=user)

        if user.is_teacher:
            return StudentEnrollment.objects.filter(course__teacher=user)

        return StudentEnrollment.objects.all()


class AssignmentCreateList(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentSubmissionPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Assignment.objects.filter(course__enrollments__student=user).distinct()

        if user.is_teacher:
            return Assignment.objects.filter(course__teacher=user)

        return Assignment.objects.all()

    def perform_create(self, serializer):
        user = cast(User, self.request.user)

        if not user.is_teacher:
            raise PermissionDenied("Only teachers can create assignments")

        course = serializer.validated_data.get("course")

        if course.teacher != user:
            raise PermissionDenied("You are not assigned to this course")

        serializer.save()


class AssignmentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentSubmissionPermission]
    lookup_url_kwarg = 'assignment_id'

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Assignment.objects.filter(course__enrollments__student=user).distinct()

        if user.is_teacher:
            return Assignment.objects.filter(course__teacher=user)

        return Assignment.objects.all()


class SubmissionCreateList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [AssignmentSubmissionPermission]

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Submission.objects.filter(student=user)

        if user.is_teacher:
            return Submission.objects.filter(assignment__course__teacher=user)

        return Submission.objects.all()

    def perform_create(self, serializer):
        user = cast(User, self.request.user)

        if not user.is_student:
            raise PermissionDenied("Only students can submit assignments")

        assignment = serializer.validated_data.get("assignment")

        if not assignment.course.enrollments.filter(student=user).exists():
            raise PermissionDenied("You are not enrolled in this course")

        serializer.save(student=user, status=StatusChoices.SUBMITTED)


class SubmissionRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [AssignmentSubmissionPermission]
    lookup_url_kwarg = 'submission_id'

    def get_queryset(self):
        user = cast(User, self.request.user)

        if user.is_student:
            return Submission.objects.filter(student=user)

        if user.is_teacher:
            return Submission.objects.filter(assignment__course__teacher=user)

        return Submission.objects.all()

    def perform_destroy(self, instance):
        user = cast(User,self.request.user)

        if not user.is_teacher:
            raise PermissionDenied("Only teachers can delete submissions")

        if instance.assignment.course.teacher != user:
            raise PermissionDenied("Not your course")

        instance.delete()