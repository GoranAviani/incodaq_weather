#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mobile_phone.models import user_phone


def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      return render(request,'index.html')

def dashboard(request):
   if request.user.is_authenticated:
      

      dashboardStatus = "Hi, welcome to your dashboard."
      statusColor = "green"
  
      
      userMobileNumber = User.objects.filter(userMobilePhone=request.user)
     # queryUserNote = note.objects.filter(noteUser=request.user).order_by('-noteTimestamp')
      return render(request, 'dashboard.html', 
      {
      'dashboardStatus':dashboardStatus,
      'statusColor': statusColor,
      'userMobileNumber': userMobileNumber,
     # 'queryUserNote': queryUserNote,
      })


   else:
        #if user is not authenticated inform him of that
        return render(request, 'other_pages/not_authenticaded.html')




