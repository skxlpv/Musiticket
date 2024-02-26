from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls.base import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from api.models import BlackListedToken
from api.serializers import RegistrationSerializer, LoginSerializer
from users.models import UserModel
from django.core.exceptions import ObjectDoesNotExist


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


from django.http import HttpResponse

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
                if user is not None:
                    login(request, user)
                    print("IsAuthenticated", user.is_authenticated)

                    Token.objects.filter(user=user).delete()

                    token = Token.objects.create(user=user)

                    response = Response({'token': token.key}, status=status.HTTP_200_OK)
                    response.set_cookie('refresh_token', token.key, httponly=True)
                    return response
                else:
                    return Response({"Invalid username or password. Please try again"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Invalid input data. Please try again"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')

        if not BlackListedToken.objects.filter(token=refresh_token).first():
            BlackListedToken.objects.create(token=refresh_token, user=request.user)

        logout(request)

        response = HttpResponseRedirect(reverse('home'))
        response.delete_cookie("refresh_token")

        return response
    except ObjectDoesNotExist:
        return Response("No refresh token was provided")
