from django.urls import path
from .views import SummaryView, CategoryBreakdownView, TrendView

urlpatterns = [
    path('dashboard/summary/', SummaryView.as_view()),
    path('dashboard/category-breakdown/', CategoryBreakdownView.as_view()),
    path('dashboard/trends/', TrendView.as_view()),
]