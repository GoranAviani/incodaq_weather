from django.db import models

# Create your models here.
class default_cities(models.Model):
    Stockholm = models.CharField(max_length=50,null=True, blank=True)
    Tokyo = models.CharField(max_length=50,null=True, blank=True)
    New_York = models.CharField(max_length=50,null=True, blank=True)
    Moscow = models.CharField(max_length=50,null=True, blank=True)
    Berlin = models.CharField(max_length=50,null=True, blank=True)
    Paris = models.CharField(max_length=50,null=True, blank=True)
    Bejing = models.CharField(max_length=50,null=True, blank=True)
    Rome = models.CharField(max_length=50,null=True, blank=True)
    San_Francisco = models.CharField(max_length=50,null=True, blank=True)
    Split = models.CharField(max_length=50,null=True, blank=True)
    London = models.CharField(max_length=50,null=True, blank=True)
    Shanghai = models.CharField(max_length=50,null=True, blank=True)
    