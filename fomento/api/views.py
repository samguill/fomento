from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, permissions, generics, filters
import datetime


from fomento.models import Fomento
from .serializers import FomentoSerializer


class FomentoViewSet(viewsets.ModelViewSet):
    queryset = Fomento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FomentoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year', 'month', 'day']

