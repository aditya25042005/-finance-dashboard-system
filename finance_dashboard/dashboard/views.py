from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import DatabaseError
from rest_framework import status

from records.models import Record
from .serializers import *
from users.permissions import *
from drf_spectacular.utils import extend_schema,OpenApiParameter

##recent activity
@extend_schema(
request=SummaryRequestSerializer,
responses={200: SummaryResponseSerializer, 400: None, 500: None}


)
class SummaryView(APIView):
    permission_classes = [Viewer_Analyst_Admin]

    def post(self, request):
     serializer = SummaryRequestSerializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     data = serializer.validated_data
     try:
        queryset = Record.objects.all()

        if 'type' in data:
            queryset = queryset.filter(type=data['type'])

        if 'category' in data:
            queryset = queryset.filter(category__iexact=data['category'])

        if 'start_date' in data and 'end_date' in data:
            queryset = queryset.filter(date__range=[data['start_date'], data['end_date']])
        ## later do start date and end data > than condition
        totals = queryset.values("type").annotate(total=Sum("amount"))

        income = next((row["total"] for row in totals if row["type"] == "income"), 0) or 0
        expense = next((row["total"] for row in totals if row["type"] == "expense"), 0) or 0

        response_data = {
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
        }

        return Response(SummaryResponseSerializer(response_data).data)
     except DatabaseError:
            return Response(
                {
                    "error": "Failed to generate summary",
                 
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
     except Exception as e:
            return Response(
                {
                    "error": "An unexpected error occurred while generating summary",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    request=None,
    responses={200: CategoryBreakdownSerializer(many=True)},
)
class CategoryView(APIView):
    permission_classes = [Viewer_Analyst_Admin]

    def get(self, request):
        queryset = Record.objects.all()

        grouped = (
            queryset.values("category", "type")
            .annotate(total=Sum("amount"))
            .order_by("category", "type")
        )
############## 
        return Response(CategoryBreakdownSerializer(grouped, many=True).data)


@extend_schema(
    request=None,
    parameters=[
        OpenApiParameter(
            name="months",
            description="Number of past months to include in trend data (min 1, max 24). Default is 6.",
            required=False,
            type=int,
        ),
    ],
    responses={200: TrendSerializer(many=True)},
)
class TrendView(APIView):
    permission_classes = [Viewer_Analyst_Admin]
##MonTH ABC-edge case
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
                "month": row["month"].strftime("%b %Y"),
                "type": row["type"],
                "total": row["total"],
            }
            for row in trends
        ]

        return Response(TrendSerializer(formatted, many=True).data)
    



    ##API FOR CATEGORY AND TYPE FILTER

    #Monthly or weekly trends
#error handling and logging for wrong data type 

##insights and tagged records remaining