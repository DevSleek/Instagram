from .views import CreateUserView, UserVerifyAPIView
from django.urls import path

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', UserVerifyAPIView.as_view())
]
