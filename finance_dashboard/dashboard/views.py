from django.shortcuts import render


from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from records.models import Record


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from records.models import Record


class SummaryView(APIView):

    def post(self, request):
        queryset = Record.objects.all()

        record_type = request.data.get('type')
        category = request.data.get('category')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if record_type:
            queryset = queryset.filter(type=record_type)

        if category:
            queryset = queryset.filter(category__iexact=category)

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        totals = queryset.values("type").annotate(total=Sum("amount"))

        income = next((row["total"] for row in totals if row["type"] == "income"), 0) or 0
        expense = next((row["total"] for row in totals if row["type"] == "expense"), 0) or 0

        return Response({
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
        })
    
class CategoryBreakdownView(APIView):

    def get(self, request):
        queryset = Record.objects.all()

        grouped = (
            queryset.values("category", "type")
            .annotate(total=Sum("amount"))
            .order_by("category", "type")
        )

        return Response(grouped)


class TrendView(APIView):

    def get(self, request):
        months = int(request.query_params.get("months", 6))
        months = min(max(months, 1), 24)

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
                "month": row["month"].date().isoformat() if row["month"] else None,
                "type": row["type"],
                "total": row["total"],
            }
            for row in trends
        ]

        return Response(formatted)