from django.urls import path

from .views import PostListAPIView


urlpatterns = [
     path('post-lists/', PostListAPIView.as_view())
 ]