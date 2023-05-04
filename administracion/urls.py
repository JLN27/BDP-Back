from rest_framework import routers
from .api import ArtistViewSet, UserViewSet
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = routers.DefaultRouter()

router.register('api/artists', ArtistViewSet, 'artists')
router.register('api/users', UserViewSet, 'users')


urlpatterns = [
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls