from .models import Artist
from rest_framework import viewsets, permissions
from .serializers import ArtistSerializer
from .permissions import IsEditorOrReadOnly

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsEditorOrReadOnly]