#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User



def index(request):
#   return render(request,'index.html')

   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      return render(request,'index.html')
