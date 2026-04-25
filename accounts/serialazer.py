from django.contrib.auth import authenticate
from accounts.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Failed to login')
        return {"user": user}


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def validate(self, data):
        confirm_password = data.get('confirm_password')
        password = data.get('password')
        data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Your password not equals to confirm_password')
        return super(RegistrationSerializer, self).validate(data)

    def create(self, data):
        return User.objects.create_user(**data)


class BlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField()
