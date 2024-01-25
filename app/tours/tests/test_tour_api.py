"""
Tests for tours APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tours

from tours.serializers import (
    TourSerializer,
    TourDetailSerializer
)


TOURS_URL = reverse('tours:tours-list')


def detail_url(tour_id):
    """Create and return a tour detail URL."""
    return reverse('tours:tours-detail', args=[tour_id])


def create_superuser():
    """Create and return a sample superuser."""
    email = 'admin@example.com'
    password = 'adminpass123'

    user_model = get_user_model()

    # Check if the user already exists
    existing_user = user_model.objects.filter(email=email).first()
    if existing_user:
        return existing_user

    # Create a new superuser if it doesn't exist
    return user_model.objects.create_superuser(
        email=email,
        password=password,
    )


def create_tour(user, **params):
    """Create and return a sample tour."""
    defaults = {
        'title': 'Sample tour title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/tour.pdf',
    }
    defaults.update(params)

    tour = Tours.objects.create(user=user, **defaults)
    return tour


class PublicToursAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tours(self):
        """Test retrieving a list of Tours is available to all users."""
        create_tour(user=create_superuser())
        create_tour(user=create_superuser())

        res = self.client.get(TOURS_URL)

        tours = Tours.objects.all().order_by('-id')
        serializer = TourSerializer(tours, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateTourApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.superuser = create_superuser()
        self.client.force_authenticate(self.superuser)

    def test_retrieve_tours(self):
        """Test retrieving a list of Tours."""
        create_tour(user=self.superuser)
        create_tour(user=self.superuser)

        res = self.client.get(TOURS_URL)

        tours = Tours.objects.all().order_by('-id')
        serializer = TourSerializer(tours, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tour_list_limited_to_user(self):
        """Test list of tours is limited to authenticated user."""
        normal_user = get_user_model().objects.create_user(
            'normal@example.com',
            'password123',
        )

        with self.assertRaises(PermissionDenied):
            create_tour(user=normal_user)

        create_tour(user=self.superuser)

        res = self.client.get(TOURS_URL)

        tours = Tours.objects.filter(user=self.superuser)
        serializer = TourSerializer(tours, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_tour_detail(self):
        """Test get tour detail."""
        tour = create_tour(user=self.superuser)

        url = detail_url(tour.id)
        res = self.client.get(url)

        serializer = TourDetailSerializer(tour)
        self.assertEqual(res.data, serializer.data)
