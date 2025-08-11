from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from uuid import uuid4

from .models import User
from .serializers import UserSerializer, UserSimpleSerializer

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        nickname = request.data.get("nickname")

        if not email or not password or not nickname:
            return Response({"error": "필수 필드가 없습니다."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "이미 가입된 이메일입니다."}, status=400)

        user = User.objects.create_user(email=email, password=password, nickname=nickname, username=f"{nickname}_{uuid4().hex[:6]}")
 
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "이메일과 비밀번호를 입력해주세요."}, status=400)

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "잘못된 로그인 정보입니다."}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nickname = request.query_params.get('nickname')
        if not nickname:
            return Response({"error": "닉네임을 입력하세요."}, status=400)
        
        users = User.objects.filter(nickname__icontains=nickname).exclude(id=request.user.id)
        serializer = UserSimpleSerializer(users, many=True)
        return Response(serializer.data)