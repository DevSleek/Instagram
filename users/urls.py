from .views import CreateUserView, UserVerifyAPIView, GetNewVevification
from django.urls import path

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', UserVerifyAPIView.as_view()),
    path('new-verify/', GetNewVevification.as_view())
]
