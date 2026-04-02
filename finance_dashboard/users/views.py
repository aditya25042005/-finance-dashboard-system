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

#create user
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
        return Response({"error":str(e)},status=400)
      
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

class UserLogin(APIView):
   

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        #inactive user
        if not user.is_active:
            return Response(
                {"error": "This account is inactive"},
                status=status.HTTP_403_FORBIDDEN
            )
        #i am using django's built in session authentication
        login(request, user)

        return Response(
            {
                "message": "Login successful"
               
            },
            status=status.HTTP_200_OK
        )
    
# logout view pending