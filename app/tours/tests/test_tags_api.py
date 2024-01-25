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


def detail_url(tag_id):
    """Create and return a tag detail url."""
    return reverse('tours:tag-detail', args=[tag_id])


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

    # def test_retrieve_tags(self):
    #     """Test retrieving a list of tags by an authenticated user."""
    #     # Create a superuser
    #     superuser = create_superuser(email='superuser@example.com', password='adminpass123')

    #     # Use the superuser for testing
    #     self.client.force_authenticate(user=superuser)

    #     # Create some tags
    #     Tag.objects.create(name='Vegan')
    #     Tag.objects.create(name='Dessert')

    #     res = self.client.get(TAGS_URL)

    #     # Retrieve tags from the database
    #     tags = Tag.objects.all().order_by('-name')

    #     # Serialize tags for comparison
    #     serializer = TagSerializer(tags, many=True)

    #     # Check the response
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)


# class PrivateTagsApiTests(TestCase):
#     """Test authenticated API requests."""

#     def setUp(self):
#         self.superuser = create_superuser()
#         self.client = APIClient()
#         self.client.force_authenticate(self.superuser)

#     def test_retrieve_tags(self):
#         """Test retrieving a list of tags."""
#         Tag.objects.create(user=self.superuser, name='Vegan')
#         Tag.objects.create(user=self.superuser, name='Dessert')

#         res = self.client.get(TAGS_URL)

#         tags = Tag.objects.all().order_by('-name')
#         serializer = TagSerializer(tags, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)


# class TagApiTests(TestCase):
#     """Test tags API."""

#     def setUp(self):
#         self.client = APIClient()
#         self.superuser = create_superuser()
#         self.client.force_authenticate(user=self.superuser)

#     def test_create_tag_no_super_user(self):
#         """Test creating a new tag no superuser."""
#         payload = {'name': 'Vegan'}
#         # Try to create a tag as a non-superuser
#         non_superuser = create_user(email='test@example.com', password='testpass')
#         self.client.force_authenticate(user=non_superuser)
#         res = self.client.post(TAGS_URL, payload)

#         # Expect a 403 Forbidden response
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


#     def test_delete_tag_superuser(self):
#         """Test deleting a tag superuser."""
#         # Create a tag for the superuser
#         tag = Tag.objects.create(user=self.superuser, name='Breakfast')

#         # Attempt to delete the tag as a superuser
#         url = detail_url(tag.id)
#         res = self.client.delete(url)

#         # Expect a 204 No Content response since the superuser can delete
#         self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

#         # Check that the tag has been deleted
#         tags = Tag.objects.filter(user=self.superuser)
#         self.assertFalse(tags.exists())


# def test_delete_tag_not_superuser(self):
#         """Test deleting a tag as a non-superuser."""
#         # Create a tag for a non-superuser
#         non_superuser = create_user(email='test@example.com', password='testpass')
#         tag = Tag.objects.create(user=non_superuser, name='Lunch')

#         # Attempt to delete the tag as a non-superuser
#         url = detail_url(tag.id)
#         res = self.client.delete(url)

#         # Expect a 403 Forbidden response since the user is not a superuser
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

#         # Check that the tag has not been deleted
#         tags = Tag.objects.filter(user=non_superuser)
#         self.assertTrue(tags.exists())
