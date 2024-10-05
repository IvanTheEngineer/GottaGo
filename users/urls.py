from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('3rdparty/login/cancelled/', views.cancel_login, name='home'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('admin/', admin.site.urls),
]