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
    path('project_creator/', views.project_creation, name='project_creator'),
    path('plans/', views.user_plans_view, name='plans')
]
