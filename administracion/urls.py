from rest_framework import routers
from .api import ArtistViewSet

router = routers.DefaultRouter()

router.register('api/artists', ArtistViewSet, 'artists')

urlpatterns = router.urls