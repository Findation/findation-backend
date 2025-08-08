from django.core.management.base import BaseCommand
from django.utils import timezone
from recovery.models import TodayRecovery
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        for user in User.objects.all():
            try:
                prev = TodayRecovery.objects.get(user=user, created_at=yesterday)
                value = prev.value
            except TodayRecovery.DoesNotExist:
                value = 0

            obj, created = TodayRecovery.objects.get_or_create(
                user=user,
                created_at=today,
                defaults={'value': value}
            )

        self.stdout.write(self.style.SUCCESS("✅ Today's recovery data created successfully."))
