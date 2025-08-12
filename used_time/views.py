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
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum, Q
from django.conf import settings

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
        # 1) 파라미터 파싱
        start_str = request.query_params.get('start')
        end_str   = request.query_params.get('end')
        try:
            if start_str and end_str:
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                end_date   = datetime.strptime(end_str, '%Y-%m-%d').date()
            else:
                end_date = timezone.localdate()
                start_date = end_date - timedelta(days=6)
        except ValueError:
            return Response({'error': 'YYYY-MM-DD 형식이어야 합니다.'}, status=400)

        # 2) 날짜별 집계 (+ 이미지 모으기)
        qs = (
            UsedTime.objects
            .filter(user=request.user, created_at__date__range=(start_date, end_date))
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(
                total_seconds=Sum('used_time'),
                image_paths=ArrayAgg('image', filter=Q(image__isnull=False))  # ['aphu/..png', ...]
            )
            .order_by('day')
        )

        # 3) dict로 변환: 합계/이미지
        totals = {row['day']: int(row['total_seconds'] or 0) for row in qs}
        images_by_day = {}
        for row in qs:
            # ImageField는 .url로 풀URL 생성 가능. build_absolute_uri로 절대URL 반환
            paths = row['image_paths'] or []
            urls = []
            for p in paths:
                # p는 스토리지의 경로 문자열이므로, 임시로 객체 흉내낼 필요 없이 storage.url 사용
                # 다만 간단히는 request.build_absolute_uri(settings.MEDIA_URL + p)로도 OK
                urls.append(request.build_absolute_uri(f"{settings.MEDIA_URL}{p}"))
            images_by_day[row['day']] = urls

        # 4) zero-fill 및 응답 생성
        days = []
        cur = start_date
        while cur <= end_date:
            days.append({
                'date': cur.isoformat(),
                'used_time': totals.get(cur, 0),
                'images': images_by_day.get(cur, []),  # 그 날짜의 모든 이미지 URL 리스트
            })
            cur += timedelta(days=1)

        return Response(days, status=200)