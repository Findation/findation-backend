from rest_framework import serializers
from .models import UsedTime
from routines.serializers import RoutineSerializer

class UsedTimeSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)
    
    class Meta:
        model = UsedTime
        fields = '__all__'
        read_only_fields = ['user', 'id', 'created_at']