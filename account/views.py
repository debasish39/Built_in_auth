from django.shortcuts import render, redirect
from account.forms import RegistrationsForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email,send_reset_password_email
from django.contrib.auth import authenticate, login  # <-- import login
from .models import User
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
# from django.contrib.auth.views import LogoutView
def home(request):
    return render(request, 'account/home.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, "Both fields are required")
            return redirect("login")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid Email or Password ...")
            return redirect("login")
        if not user.is_active:
            messages.error(request, "Your account is not active. Please check your email for activation.")
            return redirect("login")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  # <-- This logs the user in!
            if user.is_seller:
                return redirect('seller_dashboard')
            elif user.is_customer:
                return redirect('customer_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid Email or Password...")
            return redirect("login")
    return render(request, 'account/login.html')

def register_view(request):
    if request.method == "POST":
        form = RegistrationsForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Or True, based on your logic
            user.save()
            
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uid64': uid64, 'token': token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email(user.email, activation_url)
            messages.success(request, "Registration successful. Please check your email for activation.")
            return redirect("login")
    else:
        form = RegistrationsForm()

    return render(request, "account/register.html", {'form': form})

def activate_account(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        if user.is_active:
            messages.warning(request, "This Account has already been activated...")
            return redirect('login')
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully.")
            return redirect('login')
        else:
            messages.error(request, "The activation link is invalid or has expired...")
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link...")   
        return redirect('login')

def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()

            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={
                    'uidb64': uidb64,
                    'token': token
                })
                absolute_reset_url=f"{request.build_absolute_uri(reset_url)}"
                # At this point, you'd send the reset_url via email
                print('Absolute Reset URL:', absolute_reset_url)
                print("Reset link:", reset_url)  # Debug only
                send_reset_password_email(user.email, absolute_reset_url)
                messages.success(request, "Password reset email sent.")
                return redirect('login')  # or wherever you want to go next

            # optional: this check is redundant if form clean_email already ensures it
            form.add_error('email', "No user found with this email.")
    
    return render(request, 'account/password_reset.html', {'form': form})

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect('password_reset')
        if request.method=="POST":
            form=SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Password reset successful. You can now login with your new password.")
                return redirect('login')
            else:
                for field,errors in form.errors.items():
                    for error in errors:
                        messages.error(request,error)
        else:
            form=SetPasswordForm(user)
        return render(request, 'account/password_reset_confirm.html', {'form': form})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "An error occur .please try again later...")
        return redirect('password_reset')    
  