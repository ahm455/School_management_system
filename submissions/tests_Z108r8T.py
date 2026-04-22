from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User, Student
from courses.models import *
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from courses.models import Course, SemesterChoices

class BaseTestCase(APITestCase):
    def setUp(self):
        self.headmaster = User.objects.create_user(
            username="admin", password="123",
            full_name="Head", email="admin@test.com",
            phone_number="03000000000", is_headmaster=True
        )

        self.teacher = User.objects.create_user(
            username="teacher", password="123",
            full_name="Teacher", email="teacher@test.com",
            phone_number="03111111111", is_teacher=True
        )

        self.student_user = User.objects.create_user(
            username="student", password="123",
            full_name="Student", email="student@test.com",
            phone_number="03222222222", is_student=True
        )

        self.student = self.student_user.student

        self.course = Course.objects.create(
            name="Math",
            code="MTH101",
            semester=SemesterChoices.FIRST,
            teacher=self.teacher,
            midterm_weightage=25,
            quiz_weightage=25,
            assignment_weightage=25,
            finalterm_weightage=25
        )


class CourseTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.create_url = reverse('courses:Course_list_create')

        self.valid_data = {
            "name": "Math",
            "code": "MTH101",
            "semester": SemesterChoices.FIRST,
            "teacher_id": self.teacher.id,
            "midterm_weightage": 30,
            "quiz_weightage": 10,
            "assignment_weightage": 10,
            "finalterm_weightage": 50
        }

    def test_headmaster_can_create_course(self):
        self.client.force_authenticate(user=self.headmaster)
        response = self.client.post(self.create_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_create_course(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.create_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_weightage(self):
        self.client.force_authenticate(user=self.headmaster)

        data = self.valid_data.copy()
        data["midterm_weightage"] = 20

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_headmaster_can_delete_course(self):
        course = Course.objects.create(
            name="Math12",code="MTH101",
            semester=SemesterChoices.FIRST,teacher=self.teacher,
            midterm_weightage=25,quiz_weightage=25,
            assignment_weightage=25,finalterm_weightage=25
        )

        url = reverse('courses:Course_detail', kwargs={'course_id': course.id})

        self.client.force_authenticate(user=self.headmaster)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_cannot_delete_course(self):
        course = Course.objects.create(
            name="Math31",code="MTH101",
            semester=SemesterChoices.FIRST,teacher=self.teacher,
            midterm_weightage=25,quiz_weightage=25,
            assignment_weightage=25,finalterm_weightage=25
        )

        url = reverse('courses:Course_detail', kwargs={'course_id': course.id})

        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EnrollmentTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.create_url = reverse('courses:Enrollment_list_create')

    def test_student_can_enroll(self):
        self.client.force_authenticate(user=self.student_user)

        data = {
            "student_id": self.student_user.id,
            "course_id": self.course.id
        }

        response = self.client.post(self.create_url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_can_delete_own_enrollment(self):
        enrollment = StudentEnrollment.objects.create(
            student=self.student_user ,
            course=self.course
        )

        url = reverse('courses:Enrollment_detail', kwargs={'enrollment_id': enrollment.id})

        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AssignmentTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('courses:Assignment_list_create')


    def test_teacher_can_create_assignment(self):
        self.client.force_authenticate(user=self.teacher)

        data = {
            "name": "HW1",
            "description": "Test",
            "course_id": self.course.id,
            "deadline": "2026-05-01"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_can_delete_assignment(self):
        assignment = Assignment.objects.create(
            name="HW1",
            description="Test",
            course=self.course,
            created_by=self.teacher,
            deadline="2026-05-01"
        )

        url = reverse('courses:Assignment_detail', kwargs={'assignment_id': assignment.id})

        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubmissionTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        StudentEnrollment.objects.create(
            student=self.student_user,
            course=self.course
        )

        self.assignment = Assignment.objects.create(
            name="HW1",
            description="Test",
            course=self.course,
            created_by=self.teacher,
            deadline="2026-05-01"
        )

        self.create_url = reverse('courses:Submission_list_create')


    def test_student_can_submit_assignment(self):
        self.client.force_authenticate(user=self.student_user)

        with open(__file__, 'rb') as file:
            data = {
                "assignment_id": self.assignment.id,
                "file": file
            }

            response = self.client.post(
                            self.create_url,data,format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 1)