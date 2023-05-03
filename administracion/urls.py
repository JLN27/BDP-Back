from rest_framework import routers
from .api import ArtistViewSet, UserViewSet, CustomAuthToken
from django.urls import path


router = routers.DefaultRouter()

router.register('api/artists', ArtistViewSet, 'artists')
router.register('api/users', UserViewSet, 'users')


urlpatterns = [
    path('api/token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
] + router.urls