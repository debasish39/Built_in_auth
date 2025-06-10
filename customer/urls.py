from django.contrib import admin
from django.urls import path
from .views import  customer_dashboard_view,password_change_view # You already imported home, no need for views.index

urlpatterns = [
    path('customer_dashboard/', customer_dashboard_view, name="customer_dashboard"),  # Use index directly
    path('password-change/',password_change_view,name="password_change")
]
