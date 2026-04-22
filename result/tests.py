from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.tests import BaseTestCase
from services.constants import SemesterChoices
from accounts.models import User
from courses.models import Course, StudentEnrollment
from result.models import Result


class ResultTest(BaseTestCase):

    def setUp(self):
        super().setUp()

        StudentEnrollment.objects.create(
            student=self.student_user,
            course=self.course
        )
        self.list_create_url = reverse("result:result_list_create")

    def create_result(self):
        return Result.objects.create(
            course=self.course,
            student=self.student_user,
            midterm_marks=20,
            assignment_marks=20,
            quiz_marks=20,
            finalterm_marks=20,
        )


    def test_teacher_can_create_result(self):
        self.client.force_authenticate(user=self.teacher)

        data = {
            "student_id": self.student_user.id,
            "course_id": self.course.id,
            "midterm_marks": 20,
            "assignment_marks": 20,
            "quiz_marks": 20,
            "finalterm_marks": 30
        }

        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_result(self):
        self.client.force_authenticate(user=self.student_user)

        data = {
            "student_id": self.student_user.id,
            "course_id": self.course.id,
            "midterm_marks": 20
        }

        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_result(self):
        result = self.create_result()

        self.client.force_authenticate(user=self.student_user)

        url = reverse("result:result_detail", kwargs={'result_id':result.id})
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_delete_result(self):
        result = self.create_result()

        self.client.force_authenticate(user=self.teacher)

        url = reverse("result:result_detail", kwargs={'result_id':result.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Result.objects.filter(id=result.id).exists(),False)

    def test_headmaster_can_view_results_only(self):
        result = self.create_result()

        self.client.force_authenticate(user=self.headmaster)

        url = reverse("result:result_detail", kwargs={'result_id':result.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)