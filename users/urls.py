from django.urls import path

from .views import CreateUserAPIView, UserVerifyAPIView, \
    GetNewVevificationAPIView, ChangeUserInfoAPIView, \
    ChangeUserPhotoAPIVIew, LoginView, LoginRefreshView, \
    LogoutAPIView, ForgotPasswordAPIView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('signup/', CreateUserAPIView.as_view()),
    path('verify/', UserVerifyAPIView.as_view()),
    path('new-verify/', GetNewVevificationAPIView.as_view()),
    path('change-user-info/', ChangeUserInfoAPIView.as_view()),
    path('change-user-photo/', ChangeUserPhotoAPIVIew.as_view())
]
