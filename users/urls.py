from django.urls import path
from .views import SocialLoginView, UserSearchView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/social-login/', SocialLoginView.as_view(), name='social-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path("search/", UserSearchView.as_view()),
]