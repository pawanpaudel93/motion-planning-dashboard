from django.urls import path, re_path, include
from .views import (
    SessionViewSet, SessionModelViewSet,
    MovementViewSet, GlobalPositionViewSet,
    GlobalHomeViewSet, LocalPositionViewSet, 
    LocalVelocityViewSet
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sessions', SessionModelViewSet, basename='sessions'),
router.register(r'session', SessionViewSet, basename='session')
router.register(r'movements', MovementViewSet, basename='movements')
router.register(r'gpositions', GlobalPositionViewSet, basename='gpositions')
router.register(r'ghomes', GlobalHomeViewSet, basename='ghomes')
router.register(r'lpositions', LocalPositionViewSet, basename='lpositions')
router.register(r'lvelocities', LocalVelocityViewSet, basename='lvelocities')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
