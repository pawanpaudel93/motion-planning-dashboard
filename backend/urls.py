"""Project Name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .api import urls as api_urls 

router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/', include(api_urls)),
    path('admin/', admin.site.urls),
]
