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


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):
        return Response({"message": "passed for {}".format(request.user.email)})
