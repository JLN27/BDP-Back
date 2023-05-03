from .models import Artist
from rest_framework import viewsets, permissions
from .serializers import ArtistSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ArtistSerializer