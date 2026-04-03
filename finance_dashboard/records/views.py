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
import logging


record_logger = logging.getLogger("record_logger")
app_logger = logging.getLogger("app_logger")
# Create your views here.


class RecordCreateAPIView(CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes=[Admin]
    authentication_classes = []

    def perform_create(self,serializer):
      try:
        ##demo
        user=User.objects.get(username=self.request.users.username)
        record=serializer.save(created_by=user)
        record_logger.info(
                f"Record created | id={record.id} | user={user.username} | type={record.type} | category={record.category} | amount={record.amount}"
            )
      except IntegrityError:
            app_logger.error(
                f"Record creation failed بسبب database constraint | user={getattr(self.request.user, 'username', 'unknown')}"
            )
            raise ValidationError({
                "detail": "Record could not be created because it violates a database constraint."
            })
      except Exception as e:
         app_logger.error(
                f"Unexpected error while creating record | user={getattr(self.request.users, 'username', 'unknown')} | error={str(e)}"
            )
       #  print(str(e))
         raise APIException("Something went wrong")

          
   


class RecordRetrieveAPIView(RetrieveAPIView):
    ##solved N+1 QUERY PROBLEM 
    queryset = Record.objects.select_related("created_by").all()
    serializer_class = RecordSerializer
    permission_classes=[Analyst_Admin]
    authentication_classes = []


   


class RecordUpdateAPIView(UpdateAPIView):
    queryset = Record.objects.all()
    permission_classes=[Admin]
    authentication_classes = []

    serializer_class = RecordSerializer


    def perform_update(self, serializer):
      

      #mock purpose change tomorrow
     
      user=User.objects.get(username=self.request.users.username)
      try:
       record=serializer.save(updated_by=user)
       record_logger.info(
                f"Record updated | id={record.id} | user={user.username}"
            )

      except IntegrityError:
          app_logger.error(
                f"Record update failed due to database constraint | user={getattr(self.request.users, 'username', 'unknown')} | record_id={getattr(self.get_object(), 'id', None)}"
            )
          raise ValidationError({
                  "detail": "Record could not be updated because it violates a database constraint."
              })



class RecordDeleteAPIView(DestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes=[Admin]
    authentication_classes = []
    def perform_destroy(self, instance):
        record_logger.info(
            f"Record deleted | id={instance.id} | user={getattr(self.request.users, 'username', 'unknown')} | type={instance.type} | category={instance.category}"
        )
        instance.delete()





class RecordListAPIView(ListAPIView):
    serializer_class = RecordSerializer
    permission_classes=[Analyst_Admin]
    pagination_class = UserPagination
    authentication_classes = []




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
            app_logger.error(
                f"Record list filtering failed | user={getattr(self.request.user, 'username', 'unknown')} | query_params={dict(self.request.query_params)} | error={str(e)}"
            )
            
            raise ValidationError({"error": "Something went wrong while filtering records."})
      




  ##bulk insert 
@extend_schema(
    request=RecordSerializer(many=True),
    responses={201: None, 400: None, 500: None}
)
class RecordBulkCreateAPIView(APIView):
    permission_classes = [Admin]
    authentication_classes = []


    def post(self, request):
        serializer = RecordSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.users)
        record_logger.info(
                f"Bulk record create success | user={request.user.username} | count={len(serializer.data)}"
            )

        return Response(
            {
                "message": "Records created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
