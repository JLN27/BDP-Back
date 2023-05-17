from rest_framework import routers
from .api import ArtistViewSet, UserViewSet, EventViewSet, SongViewSet, PlayListViewSet
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = routers.DefaultRouter()

router.register('api/artists', ArtistViewSet, 'artists')
router.register('api/users', UserViewSet, 'users')
router.register('api/events', EventViewSet, 'events')
router.register('api/songs', SongViewSet, 'songs')
router.register('api/playlists', PlayListViewSet, 'playlists')




urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls