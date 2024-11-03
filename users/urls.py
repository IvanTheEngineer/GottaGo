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
    path('destination_creator/<int:plan_id>', views.destination_creation, name='destination_creator'),
    path('all_plans/', views.all_plans_view, name='all_plans'),
    path('plans/', views.user_plans_view, name='plans'),
    path('join_group/', views.join_group, name='join_group'),
    path('download/', views.download_file, name='download_file'),
    path('deleteplan/', views.delete_travel_plan, name='delete_travel_plan'),
    path('leaveplan/', views.leave_plan, name='leave_travel_plan'),
    path("plans/<str:pk>/", views.DetailView.as_view(), name="detail"),
]

# Look into regular expressions, adding a component to that to include the travel plan id in that