from django.urls import path

from .views import PostListAPIView, PostCreateAPIView, CommentListCreateAPIView, \
    PostRetrieveUpdateDestroyAPIView, PostCommentListAPIView, PostCommentCreateAPIView, PostLikeListAPIView


urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('create/', PostCreateAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListAPIView.as_view()),
    path('<uuid:pk>/comment/create/', PostCommentCreateAPIView.as_view()),
    path('<uuid:pk>/likes', PostLikeListAPIView.as_view()),

    path('comments/', CommentListCreateAPIView.as_view())
 ]