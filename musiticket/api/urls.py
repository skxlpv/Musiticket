from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import RegistrationView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', RegistrationView.as_view(), name='registration'),
]