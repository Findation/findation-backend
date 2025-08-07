from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Interest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interests'
    )
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.user.username} - {self.name}: {self.value}"