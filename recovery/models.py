import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class TodayRecovery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    value = models.FloatField(default=0.0)

    class Meta:
        unique_together = ['user', 'created_at']
