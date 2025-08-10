from django.urls import path
from .views import UsedTimeView

urlpatterns = [
    path('', UsedTimeView.as_view()),
]