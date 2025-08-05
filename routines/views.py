from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import RoutineSerializer
from .models import Routine

# Create your views here.
class RoutineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        routines = Routine.objects.filter(user=request.user)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RoutineDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Routine, pk=pk, user=user)

    def get(self, request, pk):
        routine = self.get_object(pk, request.user)
        serializer = RoutineSerializer(routine)
        return Response(serializer.data)

    def patch(self, request, pk):
        routine = self.get_object(pk, request.user)
        serializer = RoutineSerializer(routine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        routine = self.get_object(pk, request.user)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)