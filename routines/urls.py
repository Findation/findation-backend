from django.urls import path
from .views import RoutineView, RoutineDetailView

urlpatterns = [
    path('', RoutineView.as_view()),
    path('<uuid:pk>/', RoutineDetailView.as_view()),  # ← uuid 필터링
]