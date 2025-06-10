
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("account.urls")),
    path('custo/',include("customer.urls")),
    path('sell/',include("seller.urls"))
]
