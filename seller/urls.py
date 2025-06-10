from django.contrib import admin
from django.urls import path
from .views import  seller_dashboard_view # You already imported home, no need for views.index

urlpatterns = [
    path('sell_dashboard/', seller_dashboard_view, name='seller_dashboard'),  # Use index directly
    
]
