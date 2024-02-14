from django.db import models


class UserStatusEnum(models.TextChoices):
    ONLINE = '1', 'Online'
    OFFLINE = '0', 'Offline'


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True)
    intra_id = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    profile_image = models.ImageField()
    win_count = models.IntegerField(default=0)
    lose_count = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)  # 생성 시간 자동 설정
    updated_time = models.DateTimeField(auto_now=True)      # 업데이트 시간 자동 설정
    status = models.CharField(max_length=2, choices=UserStatusEnum.choices)  # max_length 수정