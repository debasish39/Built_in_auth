from django.contrib import admin
from django.urls import path
from .views import home  # You already imported home, no need for views.index
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', home, name='home'),  # Use index directly
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('activate/<str:uid64>/<str:token>/',views.activate_account,name='activate'),
    path('password_reset/',views.password_reset_view,name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',views.password_reset_confirm_view,name='password_reset_confirm'),
    path('logout/',LogoutView.as_view(),name='logout')
]
