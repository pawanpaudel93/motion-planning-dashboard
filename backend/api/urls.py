from django.urls import path, re_path, include
from .views import SessionViewSet, SessionModelViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sessions', SessionModelViewSet, basename='session'),
router.register(r'session', SessionViewSet, basename='session')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
