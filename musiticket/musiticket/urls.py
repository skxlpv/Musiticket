from django.contrib import admin
from django.urls import path, include

from users import urls as user_profile_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', include(user_profile_urls))
]
