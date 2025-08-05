from rest_framework import serializers
from .models import Routine

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ['id', 'title', 'category', 'created_at', 'is_repeated', 'user']

        read_only_fields = ['id', 'created_at', 'user']