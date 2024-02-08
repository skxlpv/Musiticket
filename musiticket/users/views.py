from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import UserModel
from rest_framework import generics

from users.serializers import UserSerializer


class UserListView(generics.ListAPIView):
    model = UserModel
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({"error": "JWT token not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "You are authorized.", "token": token})

