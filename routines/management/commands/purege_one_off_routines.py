from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo
from routines.models import Routine

class Command(BaseCommand):
    help = "Delete one-off routines (is_repeated=0) created before today's midnight (server TZ)."

    def handle(self, *args, **options):
        tz = ZoneInfo(getattr(settings, "TIME_ZONE", "Asia/Seoul"))
        now_local = timezone.now().astimezone(tz)
        today_midnight_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_utc = today_midnight_local.astimezone(ZoneInfo("UTC"))

        qs = Routine.objects.filter(is_repeated=0, created_at__lt=cutoff_utc)
        deleted = qs.count()
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Purged {deleted} one-off routines"))