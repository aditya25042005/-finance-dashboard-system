
from rest_framework import serializers
from .models import Insight

class InsightSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Insight
        fields = ['id', 'title', 'description', 'created_by', 'created_at']
        read_only_fields = ['id',  'created_at']
        