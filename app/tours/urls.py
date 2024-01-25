"""
URL mappings for the tour app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from tours import views


router = DefaultRouter()
router.register('tours', views.TourViewSet)
router.register('tags', views.TagViewSet)

app_name = 'tours'

urlpatterns = [
    path('', include(router.urls)),
]
