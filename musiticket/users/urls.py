from django.urls import path

from users.models import UserModel
from users.views import UserListView

urlpatterns = [
    path('', UserListView.as_view(queryset=UserModel.objects.all())),
    # path('me', ),
]
