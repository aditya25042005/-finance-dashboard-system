from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from records.models import Record
from .serializers import (
    SummaryRequestSerializer,
    SummaryResponseSerializer,
    CategoryBreakdownSerializer,
    TrendSerializer
)


class SummaryView(APIView):

    def post(self, request):
        serializer = SummaryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        queryset = Record.objects.all()

        if 'type' in data:
            queryset = queryset.filter(type=data['type'])

        if 'category' in data:
            queryset = queryset.filter(category__iexact=data['category'])

        if 'start_date' in data and 'end_date' in data:
            queryset = queryset.filter(date__range=[data['start_date'], data['end_date']])

        totals = queryset.values("type").annotate(total=Sum("amount"))

        income = next((row["total"] for row in totals if row["type"] == "income"), 0) or 0
        expense = next((row["total"] for row in totals if row["type"] == "expense"), 0) or 0

        response_data = {
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
        }

        return Response(SummaryResponseSerializer(response_data).data)


class CategoryBreakdownView(APIView):

    def get(self, request):
        queryset = Record.objects.all()

        grouped = (
            queryset.values("category", "type")
            .annotate(total=Sum("amount"))
            .order_by("category", "type")
        )
############## 
        return Response(CategoryBreakdownSerializer(grouped, many=True).data)


class TrendView(APIView):

    def get(self, request):
        months = int(request.query_params.get("months", 6))
        ##edges case  24
        months = min(max(months, 1), 24)
     ## grater than case 
        from_date = timezone.now().date() - timedelta(days=months * 31)

        trends = (
            Record.objects.filter(date__gte=from_date)
            .annotate(month=TruncMonth("date"))
            .values("month", "type")
            .annotate(total=Sum("amount"))
            .order_by("month", "type")
        )

        formatted = [
            {
                "month": row["month"].date(),
                "type": row["type"],
                "total": row["total"],
            }
            for row in trends
        ]

        return Response(TrendSerializer(formatted, many=True).data)