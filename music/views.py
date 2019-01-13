from rest_framework import generics, permissions
from .models import Songs
from .serializers import SongsSerializer


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permissions = (permissions.IsAuthenticated,)
