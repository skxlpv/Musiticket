from django.contrib import admin
from django.urls import path, include

from musiticket.views import HomeView
from users import urls as user_profile_urls
from api import urls as api_urls


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('admin/', admin.site.urls),
    path('users/', include(user_profile_urls)),
    path('api/', include(api_urls))

]
