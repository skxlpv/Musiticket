from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users import models as user_profile_models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_profile_models.UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

