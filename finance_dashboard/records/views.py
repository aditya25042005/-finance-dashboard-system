from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,UpdateAPIView,DestroyAPIView
from .serializer import *
from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from users.models import User
from users.permissions import *
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .pagination import UserPagination
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
# Create your views here.


class RecordCreateAPIView(CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes=[Admin]
    def perform_create(self,serializer):
      try:
        ##demo
        user=User.objects.get(username=self.request.users.username)
        serializer.save(created_by=user)
      except IntegrityError:
            raise ValidationError({
                "detail": "Record could not be created because it violates a database constraint."
            })
      except Exception as e:
       #  print(str(e))
         raise APIException("Something went wrong")

          
   


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
    serializer_class = RecordSerializer


    def perform_update(self, serializer):
      

      #mock purpose change tomorrow
     
      user=User.objects.get(username=self.request.users.username)
      try:
       serializer.save(updated_by=user)
      except IntegrityError:
          raise ValidationError({
                  "detail": "Record could not be updated because it violates a database constraint."
              })



class RecordDeleteAPIView(DestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes=[Admin]






class RecordListAPIView(ListAPIView):
    serializer_class = RecordSerializer
    permission_classes=[Analyst_Admin]
    pagination_class = UserPagination


    def get_queryset(self):
      try:
        queryset = Record.objects.all().order_by('-date')

        search = self.request.query_params.get('search')
        record_type = self.request.query_params.get('type')
        category = self.request.query_params.get('category')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
                if start_date > end_date:
                    raise ValidationError({"date": "start_date cannot be greater than end_date."})
             
        if record_type:
            queryset = queryset.filter(type__iexact=record_type)

        if category:
            queryset = queryset.filter(category__iexact=category)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)

        if search:
            queryset = queryset.filter(
                Q(type__icontains=search) |
                Q(category__icontains=search) |
                Q(notes__icontains=search)
            )

        return queryset
      except ValidationError:
            raise
      
      except Exception:
            raise ValidationError({"error": "Something went wrong while filtering records."})
      




  ##bulk insert 
@extend_schema(
    request=RecordSerializer(many=True),
    responses={201: None, 400: None, 500: None}
)
class RecordBulkCreateAPIView(APIView):
    permission_classes = [Admin]

    def post(self, request):
        serializer = RecordSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)

        return Response(
            {
                "message": "Records created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
