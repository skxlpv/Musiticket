from django.urls import path

from users.models import UserModel
from users.views import UserListView, MyProfileView

urlpatterns = [
    path('', UserListView.as_view(queryset=UserModel.objects.all()), name='users-list'),
    path('me/', MyProfileView.as_view(), name='me'),
]
