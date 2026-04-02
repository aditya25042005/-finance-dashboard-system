

from django.urls import path
from .views import *

urlpatterns = [
    path('insights/', InsightListCreateView.as_view(), name='insight-list-create'),

    path('insights/<int:pk>/', InsightDetailView.as_view(), name='insight-detail'),

    path('my-insights/', MyInsightsView.as_view(), name='my-insights'),

    path('my-insights/<int:pk>/', MyInsightDeleteView.as_view(), name='my-insight-delete'),
]