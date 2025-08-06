from django.urls import path
from .views import FriendshipView, FriendshipDetailView

urlpatterns = [
    path('', FriendshipView.as_view()),
    path('<uuid:pk>/', FriendshipDetailView.as_view()),
]