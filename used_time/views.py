from django.shortcuts import render
from rest_framework import status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from .models import UsedTime
from .serializers import UsedTimeSerializer
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate

# Create your views here.

class UsedTimeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """사용 시간 기록"""
        serializer = UsedTimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """특정 날짜의 모든 루틴 사용 시간 조회"""
        # 날짜 파라미터 받기 (기본값: 오늘)
        date_str = request.query_params.get('date', timezone.now().date().isoformat())
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': '올바른 날짜 형식이 아닙니다. (YYYY-MM-DD)'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 해당 날짜의 시작과 끝 시간 계산
        start_datetime = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))
        
        # 해당 유저의 해당 날짜에 대한 모든 UsedTime 조회
        used_times = UsedTime.objects.filter(
            user=request.user,
            created_at__range=(start_datetime, end_datetime)
        ).order_by('created_at')
        
        serializer = UsedTimeSerializer(used_times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsedTimeRangeView(views.APIView):
    def get(self, request):
        # 파라미터 파싱
        start_str = request.query_params.get('start')
        end_str   = request.query_params.get('end')
        try:
            if start_str and end_str:
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                end_date   = datetime.strptime(end_str,   '%Y-%m-%d').date()
            else:
                # 기본: 오늘 기준 지난 6일 ~ 오늘
                end_date = timezone.localdate()
                start_date = end_date - timedelta(days=6)
        except ValueError:
            return Response({'error': 'YYYY-MM-DD 형식이어야 합니다.'}, status=400)

        # 날짜 범위 집계
        qs = (UsedTime.objects
              .filter(user=request.user, created_at__date__range=(start_date, end_date))
              .annotate(day=TruncDate('created_at'))
              .values('day')
              .annotate(total_seconds=Sum('used_time'))
              .order_by('day'))

        # zero-fill: 빠진 날짜 0으로 채우기
        totals = {row['day']: row['total_seconds'] or 0 for row in qs}

        days = []
        cur = start_date
        while cur <= end_date:
            days.append({
                'date': cur.isoformat(),
                'used_time': int(totals.get(cur, 0)),
            })
            cur += timedelta(days=1)

        return Response(days, status=200)
