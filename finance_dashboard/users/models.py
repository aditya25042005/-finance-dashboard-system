from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class  User(AbstractUser):
         roles=(
                 ('admin','Admin'),
                 ('viewer','Viewer'),
                 ('analyst','Analyst'),  )
         role=models.CharField(max_length=20,choices=roles)
    