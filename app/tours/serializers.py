"""
Serializers for tour APIs
"""
from rest_framework import serializers

from core.models import (
    Tours,
    Tag,
)


class TourSerializer(serializers.ModelSerializer):
    """Serializer for tours."""

    class Meta:
        model = Tours
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class TourDetailSerializer(TourSerializer):
    """Serializer for tour detail view."""

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ['id']
