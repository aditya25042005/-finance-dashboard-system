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
#create user

@extend_schema(
    request=UserSerializer,
    responses={201: None, 400: None}
)
class UserCreateView(APIView):
    permission_classes = [Admin]

    
    def post(self,request):
      try:
        data=request.data

        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
      except Exception as e:
        return Response({"error":str(e)},status=500)
      
#list of user paginationg pending   
class UserListView(ListAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class = UserPagination
    permission_classes = [Admin]



#each user view
class userDetailView(RetrieveAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='username'
    permission_classes = [Admin]


# update user role
## is active is also there which is not in serializer
class UserUpdateView(UpdateAPIView):
   
        queryset=User.objects.all()
        serializer_class=UserSerializer
        lookup_field='username'
        permission_classes = [Admin]


class UserDeleteView(DestroyAPIView):
        queryset=User.objects.all()
        serializer_class=UserSerializer
        lookup_field='username'
        permission_classes = [Admin]

        
   
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
            return Response(
                {"error": "Invalid credentials. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        #inactive user
        if not user.is_active:
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
        
    
