from django.urls import path

from .views import PostListAPIView, PostCreateAPIView, \
    PostRetrieveUpdateDestroyAPIView, PostCommentListAPIView, PostCommentCreateAPIView


urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('post/create/', PostCreateAPIView.as_view()),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('post/<uuid:pk>/comments/', PostCommentListAPIView.as_view()),
    path('post/<uuid:pk>/comment/create/', PostCommentCreateAPIView.as_view())
 ]