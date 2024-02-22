import os
import uuid
from django.db import models
from django.conf import settings


class UserStatusEnum(models.TextChoices):
    ONLINE = "1", "Online"
    OFFLINE = "0", "Offline"


class Users(models.Model):
    REQUIRED_FIELDS = []  # 필수 필드
    USERNAME_FIELD = "user_id"  # 고유한 식별자 필드
    is_anonymous = False  # 익명 사용자 허용 안 함
    is_authenticated = True  # 인증된 사용자만 허용

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intra_id = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images")
    win_count = models.IntegerField(default=0)
    lose_count = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)  # 생성 시간 자동 설정
    updated_time = models.DateTimeField(auto_now=True)  # 업데이트 시간 자동 설정
    status = models.CharField(max_length=2, choices=UserStatusEnum.choices)

    class Meta:
        db_table = "Users"
        ordering = ["created_time"]

    def delete(self, using=None, keep_parents=False) -> None:
        """
        delete 메서드 오버라이딩
        Args:
            using: 삭제할 때 사용할 DB, 기본값은 None으로 기본 DB를 사용
            keep_parents: 삭제 작업을 수행할 때, 자식 객체를 유지할 지 여부, 기본값은 False로 자식 객체를 삭제
        """
        if self.profile_image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.profile_image.name))
        super(Users, self).delete(using, keep_parents)


class RequestStatusEnum(models.TextChoices):
    ACCEPTED = "1", "Accept"
    PENDING = "0", "Pending"


"""
Foreign Key options
- CASCADE: 부모가 삭제되면 자식도 삭제
- db_column: DB에 저장되는 컬럼명
- related_name: 역참조 시 사용할 이름
"""


class FriendRequests(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_user_id = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE,
        db_column="request_user_id",
        related_name="from_user",
    )
    response_user_id = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE,
        db_column="response_user_id",
        related_name="to_user",
    )
    created_time = models.DateTimeField(auto_now_add=True)  # 생성 시간 자동 설정
    updated_time = models.DateTimeField(auto_now=True)  # 업데이트 시간 자동 설정
    status = models.CharField(max_length=2, choices=RequestStatusEnum.choices)

    class Meta:
        db_table = "FriendRequests"
        ordering = ["created_time"]
