from rest_framework import routers
from .api import ArtistViewSet, UserViewSet, EventViewSet, SongViewSet, PlayListViewSet, ArtistSongsList, CustomTokenObtainPairView
from django.urls import path



router = routers.DefaultRouter()

router.register('artists', ArtistViewSet, 'artists')
router.register('users', UserViewSet, 'users')
router.register('events', EventViewSet, 'events')
router.register('songs', SongViewSet, 'songs')
router.register('playlists', PlayListViewSet, 'playlists')




urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('artists/<int:artist_id>/songs/', ArtistSongsList.as_view(), name='artist-songs-list'),
] + router.urls