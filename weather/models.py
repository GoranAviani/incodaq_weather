from django.db import models

# Create your models here.
    
class default_cities(models.Model):
    city = models.CharField(max_length=50,null=True, blank=True)
    temperature = models.CharField(max_length=50, null=True, blank=True)
   