from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .pagination import UserPagination
from .serializers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,UpdateAPIView,DestroyAPIView
from django.contrib.auth import authenticate, login
from .permissions import *
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from drf_spectacular.utils import extend_schema
import logging
auth_logger = logging.getLogger("auth_logger")
app_logger = logging.getLogger("app_logger")
#create user

@extend_schema(
    request=UserSerializer,
    responses={201: None, 400: None}
)
class UserCreateView(APIView):
    permission_classes = [Admin]
    authentication_classes = []

    
    def post(self,request):
      try:
        data=request.data

        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            auth_logger.info(
                    f"User created | created_by={request.users.username} | username={serializer.data['username']} | role={serializer.data['role']}"
                )
            

            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
      except Exception as e:
        app_logger.error(
                f"User creation failed | requested_by={getattr(request.users, 'username', 'anonymous')} | error={str(e)}"
            )
        return Response({"error":"error occurred"},status=500)
      
#list of user paginationg pending   
class UserListView(ListAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class = UserPagination
    permission_classes = [Admin]
    authentication_classes= []



#each user view
class userDetailView(RetrieveAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='username'
    permission_classes = [Admin]
    authentication_classes = []


# update user role
## is active is also there which is not in serializer
class UserUpdateView(UpdateAPIView):
   
        queryset=User.objects.all()
        serializer_class=UserSerializer
        lookup_field='username'
        permission_classes = [Admin]
        def perform_update(self, serializer):
          user=serializer.save()
       
          auth_logger.info(
            f"User updated | updated_by={self.request.users.username} | username={user.username}"
        )
      


class UserDeleteView(DestroyAPIView):
        queryset=User.objects.all()
        serializer_class=UserSerializer
        lookup_field='username'
        permission_classes = [Admin]
        authentication_classes = []
        def perform_destroy(self, instance):
             auth_logger.info(
            f"User deleted | deleted_by={self.request.users.username} | username={instance.username}"
        )
             instance.delete()
        


        
   
   ##auth remaining
@extend_schema(
    request=LoginSerializer,
    responses={200: None, 401: None}
)
class UserLogin(APIView):
        
   

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
       

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)

        if user is None:
            auth_logger.warning(
                f"Login failed | username={username} | reason=invalid_credentials"
            )
            return Response(
                {"error": "Invalid credentials. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        #inactive user
        if not user.is_active:
            auth_logger.warning(
                f"Login failed | username={username} | reason=invalid_credentials"
            )
            return Response(
                {"error": "This account is inactive"},
                status=status.HTTP_403_FORBIDDEN
            )
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(days=14),
            "iat": datetime.now(timezone.utc),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        auth_logger.info(
            f"Login success | username={user.username} | role={user.role}"
        )
       

        response=Response(
            {
                "message": "Login successful",
                  "access_token": token
      
               
            },
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,      # True in production with HTTPS
            samesite="Lax",
            max_age=14 * 24 * 60 * 60
        )
        return response
        
    
