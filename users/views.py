import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken

APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"

def verify_apple_token(identity_token: str):
    res = requests.get(APPLE_KEYS_URL)
    apple_keys = res.json()["keys"]
    headers = jwt.get_unverified_header(identity_token)
    kid = headers["kid"]
    alg = headers["alg"]

    key = next((k for k in apple_keys if k["kid"] == kid and k["alg"] == alg), None)
    if key is None:
        raise Exception("Apple public key not found")

    public_key = RSAAlgorithm.from_jwk(key)

    decoded = jwt.decode(
        identity_token,
        key=public_key,
        algorithms=[alg],
        audience="com.Yoy0z-maps.Findation",
        issuer="https://appleid.apple.com"
    )

    return {
        "id": decoded["sub"],
        "email": decoded.get("email")
    }

class SocialLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        provider = request.data.get("provider")
        credential = request.data.get("credential")

        if not provider or not credential:
            return Response({"error": "Provider and credential are required"}, status=400)

        try:
            if provider == "apple":
                user_info = verify_apple_token(credential["identityToken"])
            elif provider == "kakao":
                # user_info = verify_kakao_token(credential["idToken"])
                pass
            else:
                return Response({"error": "Invalid provider"}, status=400)
            
        except Exception as e:
            return Response({"error": str(e)}, status=401)

        user, created = User.objects.get_or_create(
            provider=provider,
            social_id=user_info["id"],
        )

        refresh = RefreshToken.for_user(user)

        user_data = UserSerializer(user).data

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user_data,
            "is_new_user": created,
        })