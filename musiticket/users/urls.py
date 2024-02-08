from django.urls import path

from users.models import UserModel
from users.views import UserListView, UserView

urlpatterns = [
    path('', UserListView.as_view(queryset=UserModel.objects.all()), name='users-list'),
    path('user/', UserView.as_view(), name='user'),
]
