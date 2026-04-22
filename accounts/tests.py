from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User


class AccountTest(APITestCase):

    def setUp(self):
        self.headmaster = User.objects.create_user(
            username="admin",
            password="123",
            full_name="Head Master",
            email="admin@test.com",
            phone_number="03000000000",
            is_headmaster=True
        )

        self.create_url = reverse('accounts:account_list_create')

    def test_headmaster_can_create_user(self):
        self.client.force_authenticate(user=self.headmaster)

        data = {
            "username": "ali",
            "password": "123",
            "full_name": "Ali",
            "email": "ali@test.com",
            "phone_number": "03111111111"
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_non_headmaster_cannot_create_user(self):
        teacher = User.objects.create_user(
            username="teacher",
            password="123",
            full_name="Teacher",
            email="teacher@test.com",
            phone_number="03222222222",
            is_teacher=True
        )

        self.client.force_authenticate(user=teacher)

        data = {
            "username": "test",
            "password": "123",
            "full_name": "Test User",
            "email": "test@test.com",
            "phone_number": "03000000001"
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_own_account(self):
        user = User.objects.create_user(
            username="ali",
            password="123",
            full_name="Ali",
            email="ali@test.com",
            phone_number="03111111111"
        )

        self.client.force_authenticate(user=user)

        url = reverse('accounts:account_detail', kwargs={'user_id': user.id})

        response = self.client.patch(url, {"full_name": "Ali Updated"})

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.full_name, "Ali Updated")

    def test_user_cannot_update_other_user(self):
        user1 = User.objects.create_user(
            username="user1",
            password="123",
            full_name="User One",
            email="user1@test.com",
            phone_number="03333333333"
        )

        user2 = User.objects.create_user(
            username="user2",
            password="123",
            full_name="User Two",
            email="user2@test.com",
            phone_number="03444444444"
        )

        self.client.force_authenticate(user=user2)

        url = reverse('accounts:account_detail', kwargs={'user_id': user1.id})

        response = self.client.patch(url, {"full_name": "Hacked"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_account(self):
        user = User.objects.create_user(
            username="ali",
            password="123",
            full_name="Ali",
            email="ali@test.com",
            phone_number="03111111111"
        )

        self.client.force_authenticate(user=user)

        url = reverse('accounts:account_detail', kwargs={'user_id': user.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(id=user.id).exists())