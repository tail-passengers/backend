from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FriendRequests
from accounts.models import Users


class FriendListViewSetTestCase(APITestCase):
    def setUp(self):
        # 사용자 생성
        self.user1 = Users.objects.create_user(intra_id="user1")
        self.user2 = Users.objects.create_user(intra_id="user2")
        self.user3 = Users.objects.create_user(intra_id="user3")

        # 친구 요청 생성
        FriendRequests.objects.create(
            request_user_id=self.user1,
            response_user_id=self.user2,
            status="0",
        )
        FriendRequests.objects.create(
            request_user_id=self.user1,
            response_user_id=self.user3,
            status="1",
        )

    def test_get_list_all_without_authenticate(self):
        """
        인증 없이 친구 요청 리스트 확인 시, 403 에러 확인
        """
        url = reverse(
            "friend_list", kwargs={"user_id": self.user1.user_id, "status": "all"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_all(self):
        """
        전체 친구 요청 리스트 확인
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "friend_list", kwargs={"user_id": self.user1.user_id, "status": "all"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_list_pending(self):
        """
        pending 친구 요청 리스트 확인
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "friend_list", kwargs={"user_id": self.user1.user_id, "status": "pending"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_accepted(self):
        """
        accepted 친구 요청 리스트 확인
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "friend_list", kwargs={"user_id": self.user1.user_id, "status": "accepted"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
