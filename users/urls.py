from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('3rdparty/login/cancelled/', views.cancel_login, name='home'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('project_creator/', views.project_creation, name='project_creator'),
    path('destination_creator/<str:primary_group_code>', views.destination_creation, name='destination_creator'),
    path('all_plans/', views.all_plans_view, name='all_plans'),
    path('explore_plans/', views.explore_plans_view, name='explore_plans'),
    path('plans/', views.user_plans_view, name='plans'),
    path('join_group/', views.join_group, name='join_group'),
    path('download/', views.download_file, name='download_file'),
    path('deleteplan/', views.delete_travel_plan, name='delete_travel_plan'),
    path('deletedestination/', views.delete_destination, name='delete_destination'),
    path('leaveplan/', views.leave_plan, name='leave_travel_plan'),
    path("plans/<str:primary_group_code>/", views.DetailView.as_view(), name="detail"),
    path("plans/<str:primary_group_code>/destination/<str:id>/", views.DestinationView.as_view(), name="destinations"),
    path("joinrequests/", views.joinrequests, name='joinrequests'),
    path('accept_invite/', views.accept_invite, name='accept_invite'),
    path('decline_invite/', views.decline_invite, name='decline_invite'),
    path("plans/<str:primary_group_code>/edit", views.TravelPlanUpdateView.as_view(), name="edit"),
    path("plans/<str:primary_group_code>/edit_destination/<int:id>", views.DestinationUpdateView.as_view(), name="edit_destination"),
    path("plans/<str:primary_group_code>/destination/<int:id>/", views.DestinationView.as_view(), name="destination_detail"),
    path('plans/<str:primary_group_code>/destination/<int:id>/budget/', views.destination_budget, name='destination_budget'),
    path('plans/<str:primary_group_code>/destination/<int:id>/expense/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('plans/<str:primary_group_code>/destination/<int:id>/save-location/<int:destination_id>/', views.save_location, name='save_location'),
]

# Look into regular expressions, adding a component to that to include the travel plan id in that