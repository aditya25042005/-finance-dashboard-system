from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Record
        fields = [
            "id",
            "created_by",
            "updated_by",
            "amount",
            "type",
            "category",
            "date",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]