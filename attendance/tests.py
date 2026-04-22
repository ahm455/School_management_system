from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from courses.models import Course, StudentEnrollment, SemesterChoices
from attendance.models import Attendance
from services.constants import AttentanceChoices
from courses.tests import BaseTestCase



class AttendanceTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        StudentEnrollment.objects.create(
            student=self.student_user,
            course=self.course
        )

        self.list_create_url = reverse('attendance:customer_list_create')


    def test_teacher_can_create_attendance(self):
        self.client.force_authenticate(user=self.teacher)

        data = {
            "course_id": self.course.id,
            "student_id": self.student_user.id,
            "status": AttentanceChoices.PRESENT
        }

        response = self.client.post(self.list_create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)

    def test_student_cannot_create_attendance(self):
        self.client.force_authenticate(user=self.student_user)

        data = {
            "course_id": self.course.id,
            "student_id": self.student_user.id,
            "status": AttentanceChoices.PRESENT
        }

        response = self.client.post(self.list_create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_delete_attendance(self):
        attendance = Attendance.objects.create(
            course=self.course,
            student=self.student_user,
            status=AttentanceChoices.PRESENT
        )

        url = reverse('attendance:customer_detail',kwargs={'Attendance_id': attendance.id})

        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendance.objects.count(), 0)


    def test_student_cannot_delete_attendance(self):
        attendance = Attendance.objects.create(
            course=self.course,
            student=self.student_user,
            status=AttentanceChoices.PRESENT)

        url = reverse('attendance:customer_detail',kwargs={'Attendance_id': attendance.id})

        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(url)

        self.assertIn(response.status_code,[status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])