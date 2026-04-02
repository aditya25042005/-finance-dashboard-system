from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,UpdateAPIView,DestroyAPIView
from .serializer import *
from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from users.models import User
from users.permissions import *

# Create your views here.


class RecordCreateAPIView(CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes=[Admin]
    def perform_create(self, serializer):
      try:
        ##demo
        user=User.objects.get(username='adityakarn')
        serializer.save(created_by=user)
      except Exception as e:
         print(str(e))
         raise APIException("Something went wrong", str(e))

          
   


class RecordRetrieveAPIView(RetrieveAPIView):
    ##solved N+1 QUERY PROBLEM 
    queryset = Record.objects.select_related("created_by").all()
    serializer_class = RecordSerializer
    permission_classes=[Analyst_Admin]

    ###  to do this  error handling
    
  #  http://127.0.0.1:8000/records/view/dd
   
   # then ultimate error handling


class RecordUpdateAPIView(UpdateAPIView):
    queryset = Record.objects.all()
    permission_classes=[Admin]

    def perform_update(self, serializer):
      

      #mock purpose change tomorrow
      user=User.objects.get(username='adityakarn')

      serializer.save(updated_by=user)

    serializer_class = RecordSerializer


class RecordDeleteAPIView(DestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes=[Admin]

