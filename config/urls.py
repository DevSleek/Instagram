from rest_framework_simplejwt.views import TokenBlacklistView

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
