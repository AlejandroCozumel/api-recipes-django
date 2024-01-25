"""
Views for the tour APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from core.models import (
    Tours,
    Tag,
)
from tours import serializers


class TourViewSet(viewsets.ModelViewSet):
    """View for manage tours APIs."""
    serializer_class = serializers.TourDetailSerializer
    queryset = Tours.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve tours for all users."""
        return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TourSerializer
        elif self.action == 'retrieve':
            return serializers.TourDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tour."""
        if not self.request.user.is_superuser:
            error_response = {'error': 'Only superusers can create tours.'}
            return Response(error_response, status=status.HTTP_403_FORBIDDEN)

        tour = serializer.save(user=self.request.user)

        # Return the created tour
        return tour


class CreateRetrieveTagPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user and request.user.is_superuser
        return False


class TagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateRetrieveTagPermission]

    def get_queryset(self):
        """Filter queryset to all users."""
        return self.queryset.all().order_by('-name')

    def create(self, request, *args, **kwargs):
        """Create a new tag."""
        if not request.user.is_superuser:
            error_response = {'error': 'Only superusers can create tags.'}
            return Response(error_response, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        """Delete a tag."""
        if not request.user.is_superuser:
            error_response = {'error': 'Only superusers can delete tags.'}
            return Response(error_response, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
