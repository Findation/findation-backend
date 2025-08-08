from rest_framework import serializers
from .models import TodayRecovery

class RecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodayRecovery
        fields = ['id', 'created_at', 'value', 'user']

        read_only_fields = ['id', 'created_at', 'user']