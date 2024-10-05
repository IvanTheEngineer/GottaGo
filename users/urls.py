from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('3rdparty/login/cancelled/', views.cancel_login, name='logout'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
]