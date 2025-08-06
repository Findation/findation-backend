from django.urls import path
from .views import FriendshipView, FriendshipDetailView, FriendListView, FriendRoutineView

urlpatterns = [
    path('', FriendshipView.as_view()),
    path('list/', FriendListView.as_view()), 
    path('routine/<uuid:friend_id>/', FriendRoutineView.as_view()),  
    path('<uuid:pk>/', FriendshipDetailView.as_view()),
]