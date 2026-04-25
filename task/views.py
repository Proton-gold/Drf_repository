from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, filters
from rest_framework.views import APIView
from task.models import Project, Task
from task.serialezers import ProjectlistSerializer, ProjectCreateSerializer, TaskSerializer
from django.contrib.postgres.search import TrigramSimilarity


class ProjectView(APIView):
    # def get(self, request):
    #     projects = Project.objects.all()
    #     serializer = ProjectlistSerializer(projects, many=True)
    #     return JsonResponse(serializer.data, safe=False)
    # class HelloViewSet(viewsets.ViewSet):
    #     def list(self, request):
    #         return Response({'message': 'Hello!'})

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



class TaskViewSets(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = ProjectlistSerializer

    def get_queryset(self):
        q = self.request.query_params.get('search')
        qs = Task.objects.all()
        if q:
            qs = qs.annotate(
                similarity=TrigramSimilarity(
                    'name', q
                )
            ).filter(
                similarity__gt=0.3  # 30%
            ).order_by('-similarity')
        return qs


class TaskViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = (filters.OrderingFilter,
                       filters.SearchFilter,
                       DjangoFilterBackend,)

    search_fields = [
        "title",
        "description",
    ]

    filterset_fields = [
        'status',
        'assigned_to',
    ]
