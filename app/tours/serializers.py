"""
Serializers for tour APIs
"""
from rest_framework import serializers

from core.models import Tours


class TourSerializer(serializers.ModelSerializer):
    """Serializer for tours."""

    class Meta:
        model = Tours
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']
