from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Interest
from .serializers import InterestSerializer


class InterestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interests = Interest.objects.filter(user=request.user)
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InterestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Interest, pk=pk, user=user)

    def get(self, request, pk):
        interest = self.get_object(pk, request.user)
        serializer = InterestSerializer(interest)
        return Response(serializer.data)

    def patch(self, request, pk):
        interest = self.get_object(pk, request.user)
        serializer = InterestSerializer(interest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        interest = self.get_object(pk, request.user)
        interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

