from rest_framework import serializers

from .models import Post, PostLike, PostComment, CommentLike
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'photo'
        ]


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'image',
            'caption',
            'created_time',
            'post_likes_count',
            'post_comments_count',
            'me_liked'
        ]
        extra_kwargs = {"image": {"required": False}}

    def get_post_likes_count(self, obj):
        return obj.post_likes.count()

    def get_post_comments_count(self, obj):
        return obj.post_comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                PostLike.objects.get(post=obj, author=request.user)
                return True
            except PostLike.DoesNotExist:
                return False

        return False


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    me_liked = serializers.SerializerMethodField('get_me_liked')
    comment_likes_count = serializers.SerializerMethodField('get_comment_likes_count')

    class Meta:
        model = PostComment
        fields = [
            'id',
            'author',
            'post',
            'parent',
            'content',
            'created_time',
            'replies',
            'comment_likes_count',
            'me_liked'
        ]

    def get_replies(self, obj):
        if obj.child.exists():
            serializer = self.__class__(obj.child.all(), many=True, context=self.context)
            return serializer.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.comment_likes.filter(author=user).exists()
        else:
            return False

    def get_comment_likes_count(self, obj):
        return obj.comment_likes.count()


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = [
            'id',
            'author',
            'comment'
        ]


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = [
            'id',
            'author',
            'post'
        ]