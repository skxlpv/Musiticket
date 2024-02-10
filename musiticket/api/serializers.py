from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import UserModel


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate_username(self, value):
        return value

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')
