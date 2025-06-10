from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def customer_dashboard_view(request):
    return render(request,'customer/dashboard.html')
@login_required #It is used to check whether the user is logged in or not if not it will redirect to login page and don't access the password chagne url without login...
def password_change_view(request):
    if request.method=="POST":
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request,"Password changed successfully")
            return redirect("login")
        else:
             for fields,errors in form.errors.items():
                 for error in errors:
                     messages.error(request,error)
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'customer/password_change.html')