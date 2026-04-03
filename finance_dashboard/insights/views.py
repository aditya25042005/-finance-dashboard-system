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

###users only inighTs by analyst
class MyInsightsView(ListAPIView):
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]


    def get_queryset(self):
        return Insight.objects.filter(created_by=self.request.user).order_by('-created_at')

##all insights 
class InsightListCreateView(ListCreateAPIView):
    queryset = Insight.objects.all().order_by('-created_at')
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

##each insight view
class InsightDetailView(RetrieveAPIView):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]

##delete insight only by creator no admin
class MyInsightDeleteView(DestroyAPIView):
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]

    def get_queryset(self):
        return Insight.objects.filter(created_by=self.request.user)
    

##All insights with filter and search
class InsightListAPIView(ListAPIView):
    serializer_class = InsightSerializer
    permission_classes = [Analyst_Admin]

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
            raise ValidationError(
                {"error": "Something went wrong"}
            )