from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentLikeSerializer, CommentSerializer


class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Post.objects.all()