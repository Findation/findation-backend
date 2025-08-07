from rest_framework import serializers
from .models import Interest

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'user', 'name', 'value']

        read_only_fields = ['id', 'user']