from django.urls import path
from .views import UsedTimeView, UsedTimeRangeView

urlpatterns = [
    path('', UsedTimeView.as_view()),
    path('range/', UsedTimeRangeView.as_view())
]