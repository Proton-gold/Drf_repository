from django.urls import path, include
from rest_framework import routers
from task import views

router = routers.DefaultRouter()

router.register('test', views.TaskViewSet, basename='hello')

urlpatterns = [
    path('',include(router.urls)),
    path('project/', views.ProjectView.as_view(), name='project_list'),
    path('project/create/', views.ProjectView.as_view(), name='project_create'),
    path('project/update/<int:pk>/', views.ProjectView.as_view(), name='project_update'),
]

