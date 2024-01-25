"""
Views for the tour APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tours
from tours import serializers


class TourViewSet(viewsets.ModelViewSet):
    """View for manage tours APIs."""
    serializer_class = serializers.TourSerializer
    queryset = Tours.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tours for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
