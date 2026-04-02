from django.urls import path

from .views import *

urlpatterns = [
    
    path('records/create/', RecordCreateAPIView.as_view(), name='record-create'),
    path('records/<int:pk>/', RecordRetrieveAPIView.as_view(), name='record-detail'),
    path('records/<int:pk>/update/', RecordUpdateAPIView.as_view(), name='record-update'),
    path('records/<int:pk>/delete/', RecordDeleteAPIView.as_view(), name='record-delete'),
]
