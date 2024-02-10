from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.middleware import csrf
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from api.serializers import RegistrationSerializer, LoginSerializer
from musiticket import settings
from users.models import UserModel
from users.serializers import UserSerializer


# Create your views here.
class RegistrationView(CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = UserModel.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()

            token = Token.objects.create(user=user)

            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # new_data = serializer.data
            if serializer.data:
                user = authenticate(username=request.data['username'], password=request.data['password'])
                login(request, user)
                print("IsAuthenticated", user.is_authenticated)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},
                            status=status.HTTP_200_OK)



    # def post(self, request, *args, **kwargs):
    #     response = Response()
    #     username = request.data['username']
    #     password = request.data['password']
    #
    #     user = UserModel.objects.filter(username=username).first()
    #
    #     if user is not None:
    #         if not user.check_password(password):
    #             raise AuthenticationFailed("Incorrect password")
    #
    #         user_data = get_tokens_for_user(user)
    #         response.set_cookie(
    #             key=settings.SIMPLE_JWT['AUTH_COOKIE'],
    #             value=user_data["access"],
    #             expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
    #             secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
    #             httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
    #             samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    #         )
    #
    #         csrf.get_token(request)
    #         response.data = {"Success": "Login successfully", "id": user.id}
    #
    #         return response
    #     else:
    #         return Response(
    #             {"Invalid": "Invalid username or password!!"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )


def logout(request):
    response = HttpResponseRedirect('/api/login/')
    response.delete_cookie('access_token')
    return response
