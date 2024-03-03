from django.urls import path

from .views import CreateUserAPIView, UserVerifyAPIView, \
    GetNewVevificationAPIView, ChangeUserInfoAPIView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view()),
    path('verify/', UserVerifyAPIView.as_view()),
    path('new-verify/', GetNewVevificationAPIView.as_view()),
    path('change-user/', ChangeUserInfoAPIView.as_view())
]
