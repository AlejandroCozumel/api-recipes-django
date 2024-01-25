"""
Tests for the tags API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from tours.serializers import TagSerializer

TAGS_URL = reverse('tours:tag-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='adminpass123'):
    """Create and return a superuser."""
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """Test retrieving a list of tags by unauthenticated user."""
        user = create_user()
        Tag.objects.create(user=user, name='Vegan')
        Tag.objects.create(user=user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.superuser = create_superuser()
        self.client = APIClient()
        self.client.force_authenticate(self.superuser)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.superuser, name='Vegan')
        Tag.objects.create(user=self.superuser, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
