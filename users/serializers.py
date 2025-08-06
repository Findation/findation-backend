from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'provider', 'rank', 'total_time', 'created_at', 'social_id', 'social_email']

        read_only_fields = ['id', 'created_at']

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']