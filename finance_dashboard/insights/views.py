from django.shortcuts import render
from django.conf import settings

# Create your views here.

# insights/views.py

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView,ListAPIView, DestroyAPIView
from .models import Insight
from .serializers import InsightSerializer



###users only inighns by analyst
class MyInsightsView(ListAPIView):
    serializer_class = InsightSerializer

    def get_queryset(self):
        return Insight.objects.filter(created_by=self.request.user).order_by('-created_at')

##all insights 
class InsightListCreateView(ListCreateAPIView):
    queryset = Insight.objects.all().order_by('-created_at')
    serializer_class = InsightSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

##each insight view
class InsightDetailView(RetrieveAPIView):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer

##delete insight only by creator
##later allow for admins also
class MyInsightDeleteView(DestroyAPIView):
    serializer_class = InsightSerializer

    def get_queryset(self):
        return Insight.objects.filter(created_by=self.request.user)