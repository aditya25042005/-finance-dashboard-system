from django.urls import path

from .views import *

urlpatterns = [
    
    path('create/', RecordCreateAPIView.as_view(), name='record-create'),
    path('view/<int:pk>', RecordRetrieveAPIView.as_view(), name='record-detail'),
    path('update/<int:pk>', RecordUpdateAPIView.as_view(), name='record-update'),
    path('delete/<int:pk>', RecordDeleteAPIView.as_view(), name='record-delete'),
    path('list/', RecordListAPIView.as_view(), name='record-list'),
    path("bulk-create/", RecordBulkCreateAPIView.as_view(), name="record-bulk-create"),


]
