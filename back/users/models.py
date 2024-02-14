import uuid
from django.db import models


class UserStatusEnum(models.TextChoices):
    ONLINE = '1', 'Online'
    OFFLINE = '0', 'Offline'


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intra_id = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    profile_image = models.ImageField(null=True, blank=True) # https://django-orm-cookbook-ko.readthedocs.io/en/latest/null_vs_blank.html
    win_count = models.IntegerField(default=0)
    lose_count = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)  # 생성 시간 자동 설정
    updated_time = models.DateTimeField(auto_now=True)      # 업데이트 시간 자동 설정
    status = models.CharField(max_length=2, choices=UserStatusEnum.choices)  # max_length 수정

    class Meta:
        db_table = "Users"
        ordering = ['created_time']
