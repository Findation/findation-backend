from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    rank = models.IntegerField(default=0)
    total_time = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'username']

    def __str__(self):
        return f"{self.nickname} - {self.id}의 계정입니다"