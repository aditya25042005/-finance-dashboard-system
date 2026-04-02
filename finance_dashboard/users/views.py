from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,UpdateAPIView,DestroyAPIView

# Create your views here.



#creating user
class UserCreateView(APIView):
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

#each user view
class userDetailView(RetrieveAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='username'

# update user role
## is active is also there which is not in serializer
class UserUpdateView(UpdateAPIView):
   
        queryset=User.objects.all()
        serializer_class=UserSerializer
        lookup_field='username'

class UserDeleteView(DestroyAPIView):
        queryset=User.objects.all()
        serializer_class=UserSerializer
        lookup_field='username'

        
   
   ##auth remaining