"""
Views for the tour APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Tours
from tours import serializers


class TourViewSet(viewsets.ModelViewSet):
    """View for manage tours APIs."""
    serializer_class = serializers.TourDetailSerializer
    queryset = Tours.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tours for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TourSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tour."""
        if not self.request.user.is_superuser:
            error_response = {'error': 'Only superusers can create tours.'}
            return Response(error_response, status=status.HTTP_403_FORBIDDEN)

        serializer.save(user=self.request.user)
