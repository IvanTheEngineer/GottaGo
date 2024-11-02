from logging.config import valid_ident
from typing import Protocol
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from .forms import UserLoginForm
from .decorators import user_not_authenticated
from django.contrib.auth.decorators import login_required
from .forms import PlanForm, JoinGroupForm, DestinationForm
from django.views import generic
from .models import TravelPlan, Destination
from django.http import FileResponse
import requests
import boto3


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def custom_login(request):
    print("HERE")
    return render(request, 'users/login.html')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')

def is_pma_admin(user):
    return user.groups.filter(name='PMA').exists()

def home(request):
    user = request.user
    context = {
        'PMA': user.groups.filter(name='PMA').exists(),
    }
    return render(request, 'users/home.html', context)


def cancel_login(request):
    return redirect('home')


def project_creation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PlanForm(request.POST, request.FILES)
            if is_pma_admin(request.user):
                form.add_error(None, 'PMA administrators are not able to create a project.')
            elif form.is_valid():
                plan = form.save(commit=False, user=request.user)
                print(request.user)
                plan.user = request.user
                plan.save()
                # print(f"File uploaded to S3: {plan.jpg_upload_file.url}")
                return redirect('plans')
        else:
            form = PlanForm()
        return render(request, 'users/project_creator.html', {'form': form})
    else:
        return render(request, 'users/project_creator.html')


def destination_creation(request, plan_id):
    if request.user.is_authenticated:
        travel_plan = get_object_or_404(TravelPlan, id=plan_id, users=request.user)
        if request.method == 'POST':
            form = DestinationForm(request.POST, request.FILES)
            if is_pma_admin(request.user):
                form.add_error(None, 'PMA administrators are not able to create destinations.')
            elif form.is_valid():
                plan = form.save(commit=False, travel_plan=travel_plan, user=request.user)
                # If this doesn't work, create a destination form object.
                print(request.user)
                plan.user = request.user
                plan.travel_plan = travel_plan
                plan.save()
                return redirect('detail', travel_plan.primary_group_code)
        else:
            form = DestinationForm()
        return render(request, 'users/destination_creator.html', {'form': form, 'primary_group_code': travel_plan.primary_group_code})
    else:
        return render(request, 'users/destination_creator.html')

def delete_travel_plan(request):
    id = request.GET.get('id')
    travel_plan = get_object_or_404(TravelPlan, id=id)
    if request.user != travel_plan.user and not is_pma_admin(request.user):
        messages.error(request, 'You do not have permission to delete this plan.')
        return redirect('plans')
    travel_plan.delete()
    messages.success(request, 'Successfully deleted the plan.')
    return redirect('plans')

def user_plans_view(request):
    if request.user.is_authenticated:
        # Get all plans the user is in
        travel_plans = request.user.plans.all()
        destinations = request.user.destinations.all()
        for plan in travel_plans:
            print(plan.id)
        # return render(request, 'users/plans.html', {'travel_plans': travel_plans})

        return render(request, 'users/plans.html', {'travel_plans': travel_plans, 'destinations': destinations})
    else:
        return render(request, 'users/plans.html')


def plan_destinations_view(request):
    if request.user.is_authenticated:
        destinations = request.user.destinations.all()
        return render(request, 'users/plans.html', {'destinations': destinations})
    else:
        return render(request, 'users/plans.html')

def leave_plan(request):
    id = request.GET.get('id')
    travel_plan = get_object_or_404(TravelPlan, id=id)
    travel_plan.users.remove(request.user)
    return redirect('plans')

def join_group(request):
    if request.user.is_authenticated:
        context = {'form': JoinGroupForm()}
        if request.method == 'POST':
            form = JoinGroupForm(request.POST)
            if is_pma_admin(request.user):
                context['error_message'] = 'PMA administrators are not able to join a group.'
            elif form.is_valid():
                group_code = form.cleaned_data['group_code']
                try:
                    travelPlan = TravelPlan.objects.get(primary_group_code=group_code)
                    travelPlan.users.add(request.user)
                    context['success_message'] = 'Successfully joined the group!'
                except TravelPlan.DoesNotExist:
                    context['error_message'] = 'Invalid group code. Please try again.'
        else:
            pass
        return render(request, 'users/join_group.html', context)
    else:
        return render(request, 'users/join_group.html')

def download_file(request):
    file_url = request.GET.get('txturl')
    file_name = request.GET.get('filename')
    response = requests.get(file_url, stream=True)
    response.raise_for_status()
    return FileResponse(response.raw, as_attachment=True, filename=file_name)

class DetailView(generic.DetailView):
    model = TravelPlan
    template_name = "users/detail.html"
    context_object_name = 'travelplan'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.filter(travel_plan=self.object)
        return context
    def get_object(self):
        group_code = self.kwargs.get("pk")
        return get_object_or_404(TravelPlan, primary_group_code=group_code)