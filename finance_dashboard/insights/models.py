from django.db import models
from django.conf import settings

# Create your models here.



class Insight(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="insights_created"

)
    created_at = models.DateTimeField(auto_now_add=True)
