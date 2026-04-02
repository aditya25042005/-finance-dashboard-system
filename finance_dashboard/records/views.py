from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,UpdateAPIView,DestroyAPIView
from .serializer import *
# Create your views here.


class RecordCreateAPIView(CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RecordRetrieveAPIView(RetrieveAPIView):
    queryset = Record.objects.select_related("user").all()
    serializer_class = RecordSerializer



class RecordUpdateAPIView(UpdateAPIView):
    queryset = Record.objects.all()
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    serializer_class = RecordSerializer


class RecordDeleteAPIView(DestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

