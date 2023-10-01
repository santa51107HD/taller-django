from rest_framework import serializers
from core.models import *


class MultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multas
        fields = ('__all__')

