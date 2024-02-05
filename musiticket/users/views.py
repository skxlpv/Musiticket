from users.models import UserModel
from rest_framework import generics

from users.serializers import UserSerializer


class UserListView(generics.ListAPIView):
    model = UserModel
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


