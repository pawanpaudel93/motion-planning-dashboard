"""PX4-AUTOPILOT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from .api import urls as api_urls
from .api.views import index_view

router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/', include(api_urls)),
    path('admin/', admin.site.urls),
    re_path(r'^.*$', index_view, name='index')
]
