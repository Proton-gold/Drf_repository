from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from task.models import Project, Task
from task.serialezers import ProjectlistSerializer, ProjectCreateSerializer


class ProjectView(APIView):
    # def get(self, request):
    #     projects = Project.objects.all()
    #     serializer = ProjectlistSerializer(projects, many=True)
    #     return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectCreateSerializer(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class HelloViewSet(viewsets.ViewSet):
#     def list(self, request):
#         return Response({'message': 'Hello!'})

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = ProjectlistSerializer
