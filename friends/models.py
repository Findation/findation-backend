from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Friends(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_friend_requests",)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_friend_requests",)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')  # 중복 요청 방지
        constraints = [
            models.CheckConstraint(check=~models.Q(user=models.F('friend')), name='prevent_self_friend') # 자기자신 친구 추가 방지
        ]

    def __str__(self):
        return f"{self.user} -> {self.friend} ({self.status})"