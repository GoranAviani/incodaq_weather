from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class custom_user(AbstractUser):
    userMobileNumber = models.CharField(max_length=50,null=True, blank=True)
    userAddress = models.CharField(max_length=30,null=True, blank=True)
    userCity = models.CharField(max_length=30,null=True, blank=True)
   # userCountry = models.CharField(max_length=30,null=True, blank=True)
    userCountry = CountryField(blank=True)
    userLatitude = models.CharField(max_length=30,null=True, blank=True)
    userLongitude = models.CharField(max_length=30,null=True, blank=True)
    userTimeZone = models.CharField(max_length=4)
    #userSecondEmail = models.EmailField(max_length=50,null=True, blank=True)


    def __str__(self):
        #return self.email
        return u"%s %s %s" % (self.username, self.email, self.userCountry)




