from rest_framework import serializers
from users import models as user_profile_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_profile_models.UserModel
        fields = ['first_name', 'last_name', 'date_of_birth',
                  'email', 'password', 'creation_date']
