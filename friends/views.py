# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Friends
from .serializers import FriendshipSerializer
from users.models import User
from users.serializers import UserSimpleSerializer
from routines.models import Routine
from routines.serializers import RoutineSerializer
from django.db import models

class FriendshipView(APIView):
    permission_classes = [IsAuthenticated]

    # 친구 요청 리스트 조회 (내가 보낸 것 + 받은 것)
    def get(self, request):
        user = request.user
        sent = Friends.objects.filter(user=user)
        received = Friends.objects.filter(friend=user)
        friendships = sent.union(received)
        serializer = FriendshipSerializer(friendships, many=True)
        return Response(serializer.data)

    # 친구 요청 보내기
    def post(self, request):
        user = request.user
        friend_id = request.data.get("friend_id")

        # 유효성 검사
        if not friend_id:
            return Response({"error": "friend_id는 필수입니다."}, status=400)
        if str(user.id) == str(friend_id):
            return Response({"error": "자기 자신에게 친구 요청을 보낼 수 없습니다."}, status=400)
        if Friends.objects.filter(user=user, friend_id=friend_id).exists():
            return Response({"error": "이미 요청을 보냈습니다."}, status=400)

        try:
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return Response({"error": "해당 유저를 찾을 수 없습니다."}, status=404)

        friendship = Friends.objects.create(user=user, friend=friend, status='pending')
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=201)


class FriendshipDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        user = request.user
        try:
            friendship = Friends.objects.get(id=pk, friend=user)
        except Friends.DoesNotExist:
            return Response({"error": "요청을 찾을 수 없습니다."}, status=404)

        action = request.data.get("action")  # 'accept' or 'reject'
        if action == "accept":
            friendship.status = "accepted"
        elif action == "reject":
            friendship.status = "rejected"
        else:
            return Response({"error": "올바른 action 값을 입력해주세요 (accept/reject)."}, status=400)

        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        try:
            friendship = Friends.objects.get(id=pk, user=user)
        except Friends.DoesNotExist:
            return Response({"error": "삭제할 요청이 없습니다."}, status=404)

        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendListView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 실제 친구 목록만 조회 (accepted 상태)
    def get(self, request):
        user = request.user
        # 내가 보낸 요청 중 accepted된 것들
        sent_accepted = Friends.objects.filter(user=user, status='accepted')
        # 내가 받은 요청 중 accepted된 것들  
        received_accepted = Friends.objects.filter(friend=user, status='accepted')
        
        friends = set()  # set을 사용해서 중복 제거
        for friendship in sent_accepted:
            friends.add(friendship.friend)
        for friendship in received_accepted:
            friends.add(friendship.user)
        
        # 나 자신도 추가
        friends.add(user)
        
        # set을 list로 변환
        friends_list = list(friends)
            
        serializer = UserSimpleSerializer(friends_list, many=True)
        return Response(serializer.data)


class FriendRoutineView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 친구의 루틴 보기 (친구 인증 확인 후)
    def get(self, request, friend_id):
        user = request.user
        
        # 친구 관계 확인
        is_friend = Friends.objects.filter(
            models.Q(user=user, friend_id=friend_id, status='accepted') |
            models.Q(user_id=friend_id, friend=user, status='accepted')
        ).exists()
        
        if not is_friend:
            return Response({"error": "친구가 아닙니다."}, status=403)
        
        try:
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return Response({"error": "해당 유저를 찾을 수 없습니다."}, status=404)
        
        routines = Routine.objects.filter(user=friend)
        serializer = RoutineSerializer(routines, many=True)
        
        return Response({
            "friend": UserSimpleSerializer(friend).data,
            "routines": serializer.data
        })