from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Provider(models.TextChoices):
    KAKAO = "kakao"
    GOOGLE = "google"
    APPLE = "apple"

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    provider = models.CharField(max_length=255, choices=Provider.choices, default=Provider.APPLE)
    rank = models.IntegerField(default=0)
    total_time = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)