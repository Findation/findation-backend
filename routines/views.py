from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RoutineSerializer
from .models import Routine

# Create your views here.
class RoutineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        routines = Routine.objects.filter(user=request.user)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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