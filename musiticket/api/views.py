from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import RegistrationSerializer


# Create your views here.
class RegistrationView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
