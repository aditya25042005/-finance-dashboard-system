from django.urls import path
from .views import *

urlpatterns = [
    path('summary/', SummaryView.as_view()),
    path('category_filter/', CategoryView.as_view()),
    path('trends/', TrendView.as_view()),
]