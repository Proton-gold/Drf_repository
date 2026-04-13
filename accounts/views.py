from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions import serializers
from django.contrib.sessions.models import Session
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts.models import User
from accounts.serialazer import LoginSerializer, UserSerializer, RegistrationSerializer


class AuthViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return RegistrationSerializer
        else:
            return LoginSerializer

    def get_permissions(self):
        if self.action in ('sessions', 'logout'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializers = LoginSerializer(data=request.data)
        if serializers.is_valid():
            token = serializers.validated_data.get('token')
            return Response({'token':token}, status=status.HTTP_201_CREATED)
            # login(request, user)
            # return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({'error': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False, url_path='logout')
    def logout_user(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, )
    def sessions(self, request):
        serializers = UserSerializer(request.user)
        return Response(serializers.data)

    @action(methods=['post'], detail=False, serializer_class=RegistrationSerializer, )
    def register(self, request):
        serializers = RegistrationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
