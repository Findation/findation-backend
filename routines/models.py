from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Routine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_repeated = models.IntegerField(default=0)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="routines"  
    )