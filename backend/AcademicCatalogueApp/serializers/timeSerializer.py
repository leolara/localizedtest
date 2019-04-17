from rest_framework import serializers
from ..models import Time

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Time
