"""
Serializers for tour APIs
"""
from rest_framework import serializers

from core.models import (
    Tours,
    Tag,
    PricingOption,
    FavoriteTour
)


class TourSerializer(serializers.ModelSerializer):
    """Serializer for tours."""

    class Meta:
        model = Tours
        fields = ['id', 'title', 'time_minutes', 'link']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ['id', 'name']


class PricingOptionSerializer(serializers.ModelSerializer):
    """Serializer for pricing options."""

    class Meta:
        model = PricingOption
        fields = [
            'id', 'option_name', 'option_price',
            'special_price', 'discount_percentage', 'includes'
        ]
        read_only_fields = ['id']


class TourDetailSerializer(TourSerializer):
    """Serializer for tour detail view."""
    pricing_options = PricingOptionSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields + [
            'description', 'pricing_options', 'tags'
        ]


class FavoriteTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTour
        fields = ['id', 'user', 'tour']
        read_only_fields = ['id']
