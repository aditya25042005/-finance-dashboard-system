

from django.urls import path
from .views import *

urlpatterns = [
    path('insights/', InsightListView.as_view(), name='insight-list'),

    path('insights/<int:pk>/', InsightDetailView.as_view(), name='insight-detail'),

    path('my-insights/', MyInsightsView.as_view(), name='my-insights'),

    path('my-insights/<int:pk>/', MyInsightDeleteView.as_view(), name='my-insight-delete'),
    path('bulk_create/', InsightBulkCreateAPIView.as_view(), name='insight-bulk-create'),
]