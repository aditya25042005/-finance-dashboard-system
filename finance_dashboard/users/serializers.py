from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    class Meta:
        model=User
        
        fields=['first_name','last_name','username','password','role','is_active']
        extra_kwargs={
            'password':{'write_only':True}

        }
        


