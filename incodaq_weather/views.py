#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User



def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return render(request,'dashboard.html')
   else:
      return render(request,'index.html')

def dashboard(request):
   if request.user.is_authenticated:
      return render(request, 'dashboard.html')
   else:
        #if user is not authenticated inform him of that
        return render(request, 'other_pages/not_authenticaded.html')




