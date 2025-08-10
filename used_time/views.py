from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, date
from .models import UsedTime
from .serializers import UsedTimeSerializer

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
