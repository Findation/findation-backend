from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import TodayRecovery
from .serializers import RecoverySerializer
from datetime import date
from django.shortcuts import get_object_or_404

# Create your views here.
class TodayRecoveryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        recovery = TodayRecovery.objects.filter(user=request.user, created_at=today).first()
        if not recovery:
            return Response({'detail': '오늘 리커버리 데이터가 없습니다.'}, status=404)
        serializer = RecoverySerializer(recovery)
        return Response(serializer.data)

    def patch(self, request):
        today = date.today()
        recovery = get_object_or_404(TodayRecovery, user=request.user, created_at=today)

        recorded_time = request.data.get('recorded_time')
        completed_routines = request.data.get('completed_routines')
        total_routines = request.data.get('total_routines')

        if recorded_time is None or completed_routines is None or total_routines is None:
            return Response({'error': 'recorded_time, completed_routines, total_routines 모두 필요합니다.'}, status=400)

        try:
            recorded_time = int(recorded_time)
            completed_routines = int(completed_routines)
            total_routines = int(total_routines)
        except ValueError:
            return Response({'error': '모든 값은 정수여야 합니다.'}, status=400)

        base_value = 0.55

        if completed_routines == 0:
            delta = -base_value
        else:
            if recorded_time <= 45:
                time_factor = recorded_time / 45
            elif recorded_time >= 90:
                time_factor = 1
            else:
                time_factor = recorded_time / 90

            routine_factor = completed_routines / total_routines if total_routines > 0 else 0
            delta = base_value * time_factor * routine_factor

        recovery.value = max(0, min(100, recovery.value + delta))
        recovery.save()

        serializer = RecoverySerializer(recovery)
        return Response(serializer.data, status=200)
