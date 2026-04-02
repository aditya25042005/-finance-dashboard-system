from rest_framework import serializers
from rest_framework import serializers


class SummaryRequestSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=['income', 'expense'],
        required=False
    )
    category = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)


class SummaryResponseSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2)


class CategoryBreakdownSerializer(serializers.Serializer):
    category = serializers.CharField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


class TrendSerializer(serializers.Serializer):
    month = serializers.DateField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)