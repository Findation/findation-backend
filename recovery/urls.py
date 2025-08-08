from django.urls import path
from .views import TodayRecoveryView

urlpatterns = [
    path('today/', TodayRecoveryView.as_view(), name='today-recovery'),
]
