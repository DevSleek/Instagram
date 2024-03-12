from django.contrib import admin

from posts.models import Post, PostComment, PostLike, CommentLike


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created_time', 'caption']
    search_fileds = ['id', 'author__username', 'caption']

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'created_time']
    search_fileds = ['id', 'author__username', 'comment']

class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'created_time']
    search_fields = ['id', 'author__username']

class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'comment', 'created_time']
    search_fields = ['id', 'author__username']

admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)