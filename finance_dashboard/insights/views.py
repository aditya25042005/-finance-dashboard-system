from django.shortcuts import render
from django.conf import settings

# Create your views here.

# insights/views.py
#LATER INSIGHT GIVE tag records feature
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView,ListAPIView, DestroyAPIView
from .models import Insight
from .serializers import InsightSerializer
from users.permissions import *
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from records.pagination import *
import logging
from rest_framework.exceptions import PermissionDenied

app_logger = logging.getLogger("app_logger")
insight_logger = logging.getLogger("insight_logger")

### insights by analyst
class MyInsightsView(ListAPIView):
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]
    authentication_classes = []



    def get_queryset(self):
        return Insight.objects.filter(created_by=self.request.users).order_by('-created_at')

##all insights 
class InsightListView(ListAPIView):
    queryset = Insight.objects.all().order_by('-created_at')
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]
    pagination_class =UserPagination
    authentication_classes = []

    

##each insight view
class InsightDetailView(RetrieveAPIView):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]
    authentication_classes = []

##delete insight only by creator 

##delete action response handling pending
class MyInsightDeleteView(DestroyAPIView):
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]

    def get_queryset(self):
        return Insight.objects.filter(created_by=self.request.users)
    def perform_destroy(self, instance):

        if instance.created_by != self.request.users :
            raise PermissionDenied("You are not authorized to delete this post")
        print("hi")
        insight_logger.info(
            f"Insight deleted | id={instance.id} | title={instance.title} | deleted_by={getattr(self.request.users, 'username', 'unknown')}"
        )
        instance.delete()
    

##All insights with filter and search
class InsightListAPIView(ListAPIView):
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]
    authentication_classes = []

    def get_queryset(self):
        try:
            queryset = Insight.objects.all().order_by("-created_at")

            search = self.request.query_params.get("search")
            created_by = self.request.query_params.get("created_by")
            start_date = self.request.query_params.get("start_date")
            end_date = self.request.query_params.get("end_date")

            if start_date and end_date:
                if start_date > end_date:
                    raise ValidationError(
                        {"date": "start_date cannot be greater than end_date."}
                    )

            if created_by:
                queryset = queryset.filter(created_by__username__iexact=created_by)

            if start_date and end_date:
                queryset = queryset.filter(created_at__date__range=[start_date, end_date])
            elif start_date:
                queryset = queryset.filter(created_at__date__gte=start_date)
            elif end_date:
                queryset = queryset.filter(created_at__date__lte=end_date)

            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search)
                )

            return queryset

        except ValidationError:
            raise

        except Exception:
            app_logger.error(
                f"Insight filtering failed | user={getattr(self.request.user, 'username', 'unknown')} | query_params={dict(self.request.query_params)} | error={str(e)}"
            )
            raise ValidationError(
                {"error": "Something went wrong"}
            )
        
#bulk insertion of  insight

@extend_schema(
    request=InsightSerializer(many=True),
    responses={
        201: None,
        400: None,
        500: None,
    },
)
class InsightBulkCreateAPIView(APIView):
    permission_classes = [Analyst_Admin]
    authentication_classes = []

    def post(self, request):
        serializer = InsightSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.users)
        insight_logger.info(
                f"Bulk insight create success | user={request.users.username} | count={len(serializer.data)}"
            )

        return Response(
            {
                "message": "Insights created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )