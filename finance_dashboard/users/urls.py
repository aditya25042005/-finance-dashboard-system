
from django.urls import path
from .views import  *


urlpatterns = [
       
path('create',UserCreateView.as_view(),name='create_user'),
path('list',UserListView.as_view(),name='list_user'),
path('detail/<username>',userDetailView.as_view(),name='detail_user'),
path('update/<username>/',UserUpdateView.as_view(),name='update_user'),

]
