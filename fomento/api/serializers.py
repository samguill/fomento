from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from fomento.models import Fomento


class FomentoSerializer(serializers.ModelSerializer):
    """
        Fomento serializer
    """
    class Meta:
        model = Fomento
        fields = '__all__'
        read_only_fields = ()
