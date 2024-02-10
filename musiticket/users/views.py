from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


from users.models import UserModel
from rest_framework import generics

from users.serializers import UserSerializer


class UserListView(generics.ListAPIView):
    model = UserModel
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

        return Response({"username": username,
                         "email": email,
                         "first_name": first_name,
                         "last_name": last_name})
