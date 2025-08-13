from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    total_time = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'rank', 'total_time', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_time(self, obj):
        return obj.calculated_total_time

class UserSimpleSerializer(serializers.ModelSerializer):
    total_time = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'nickname', 'total_time']
    
    def get_total_time(self, obj):
        return obj.calculated_total_time