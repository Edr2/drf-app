from rest_framework import generics, permissions
from .models import Post
from .serializers import PostsSerializer


class ListPostsView(generics.ListAPIView):
    """
    Provides a get method handler
    """
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permissions = (permissions.IsAuthenticated,)
