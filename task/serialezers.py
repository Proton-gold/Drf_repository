from rest_framework import serializers
from accounts.serialazer import UserSerializer
from task.models import Project


class ProjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()


    def create(self,validated_data):
        return Project.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.content = validated_data.get('content',instance.content)
        instance.save()
        return instance

class ProjectlistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    owner = UserSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
