# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Friends
from .serializers import FriendshipSerializer
from users.models import User

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