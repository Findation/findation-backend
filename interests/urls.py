from django.urls import path
from .views import InterestView, InterestDetailView

urlpatterns = [
    path('', InterestView.as_view(), name='interest-list-create'),
    path('<int:pk>/', InterestDetailView.as_view(), name='interest-detail'),
]
