from django.urls import path, re_path, include
from .views import (
    SessionViewSet, SessionModelViewSet,
    MovementViewSet, DroneDataViewSet,
    SimulationData, SimulationTableData,
    GlobalPositionViewSet
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sessions', SessionModelViewSet, basename='sessions'),
router.register(r'session', SessionViewSet, basename='session')
router.register(r'movements', MovementViewSet, basename='movements')
router.register(r'drones-data', DroneDataViewSet, basename='drones-data')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path("session-data/<int:pk>" , SimulationData.as_view(), name="session-data"),
    path("table-data/<int:pk>" , SimulationTableData.as_view(), name="table-data"),
    path("global-positions/<int:pk>" , GlobalPositionViewSet.as_view(), name="global-positions")
]
