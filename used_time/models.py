from django.db import models
from users.models import User
from routines.models import Routine
import uuid

def usedtime_image_path(instance, filename):
    return f'aphu/{instance.user_id}/{filename}'

class UsedTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, blank=True)
    used_time = models.IntegerField() # 프론트에서 초단위로 받고 기록됩니다
    satisfaction = models.IntegerField() # 만족도 0~5
    image = models.ImageField(upload_to=usedtime_image_path, default="aphu/default.png")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        routine_title = self.routine.title if self.routine else "삭제된 루틴"
        return f"{self.user.username}의 {routine_title}의 사용 시간은 {self.used_time}초 입니다."