# serializers.py
from rest_framework import serializers
from .models import Friends
from users.models import User

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FriendshipSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    friend = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Friends
        fields = ['id', 'user', 'friend', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']