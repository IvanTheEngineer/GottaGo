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
from .forms import PlanForm, JoinGroupForm, DestinationForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import TravelPlan, Destination, Invite
from django.http import FileResponse
import requests
import boto3

from django.core.paginator import Paginator


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


class TravelPlanUpdateView(generic.UpdateView):
    model = TravelPlan
    form_class = PlanForm
    template_name = 'users/project_editor.html'

    def get_object(self, queryset=None):
        group_code = self.kwargs.get("primary_group_code")
        return get_object_or_404(TravelPlan, primary_group_code=group_code)

    def get_success_url(self):
        primary_group_code = self.object.primary_group_code
        return reverse_lazy('detail', kwargs={'primary_group_code': primary_group_code})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['primary_group_code'] = self.object.primary_group_code
        return context


def destination_creation(request, primary_group_code):
    if request.user.is_authenticated:
        if is_pma_admin(request.user):
            travel_plan = get_object_or_404(TravelPlan, primary_group_code=primary_group_code)
            form = DestinationForm(request.POST or None, request.FILES or None)
            if request.method == 'POST':
                form.add_error(None, 'PMA administrators are not able to create destinations.')
            return render(request, 'users/destination_creator.html',
                          {'form': form, 'primary_group_code': travel_plan.primary_group_code})
        travel_plan = get_object_or_404(TravelPlan, primary_group_code=primary_group_code, users=request.user)
        if request.method == 'POST':
            form = DestinationForm(request.POST, request.FILES)
            if form.is_valid():
                plan = form.save(commit=False, travel_plan=travel_plan, user=request.user)
                # If this doesn't work, create a destination form object.
                print(request.user)
                plan.user = request.user
                plan.travel_plan = travel_plan
                plan.save()
                return redirect('detail', travel_plan.primary_group_code)
        else:
            form = DestinationForm()
        return render(request, 'users/destination_creator.html',
                      {'form': form, 'primary_group_code': travel_plan.primary_group_code})
    else:
        return render(request, 'users/destination_creator.html')


class DestinationUpdateView(generic.UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'users/destination_editor.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(Destination, id=id)

    def get_success_url(self):
        primary_group_code = self.object.travel_plan.primary_group_code
        return reverse_lazy('detail', kwargs={'primary_group_code': primary_group_code})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['primary_group_code'] = self.kwargs.get("primary_group_code")
        return context


def delete_travel_plan(request):
    id = request.GET.get('id')
    travel_plan = get_object_or_404(TravelPlan, id=id)
    if request.user != travel_plan.user and not is_pma_admin(request.user):
        messages.error(request, 'You do not have permission to delete this plan.')
        return redirect('plans')
    travel_plan.delete()
    messages.success(request, 'Successfully deleted the plan.')
    if is_pma_admin(request.user):
        return redirect('all_plans')
    return redirect('plans')


def all_plans_view(request):
    if not is_pma_admin(request.user):
        return redirect('plans')
    all_travel_plans = TravelPlan.objects.all().prefetch_related('users')
    print(f"Plans found: {all_travel_plans.count()}")
    context = {'all_travel_plans': all_travel_plans}
    return render(request, 'users/all_plans.html', context)


@user_not_authenticated
def explore_plans_view(request):
    explore_travel_plans = TravelPlan.objects.all()
    context = {'explore_travel_plans': explore_travel_plans}
    return render(request, 'users/explore_plans.html', context)


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
                    travel_plan = get_object_or_404(TravelPlan, primary_group_code=group_code)
                    if not request.user == travel_plan.user and not request.user in travel_plan.users.all():
                        existing_invite = Invite.objects.filter(travel_plan=travel_plan,
                                                                requested_by=request.user).exists()
                        if existing_invite:
                            context['error_message'] = 'You have already sent a join request for this plan.'
                        else:
                            Invite.objects.create(travel_plan=travel_plan, requested_by=request.user,
                                                  requested_to=travel_plan.user)
                            context['success_message'] = 'Successfully sent a join request!'
                    else:
                        context['error_message'] = 'You cannot join a plan you are already in.'
                except TravelPlan.DoesNotExist:
                    context['error_message'] = 'Invalid group code. Please try again.'
        else:
            pass
        return render(request, 'users/join_group.html', context)
    else:
        return render(request, 'users/join_group.html')


def joinrequests(request):
    invites = Invite.objects.filter(requested_to=request.user)
    return render(request, 'users/requests.html', {'invites': invites})


def accept_invite(request):
    id = request.GET.get('id')
    invite = get_object_or_404(Invite, id=id)
    travel_plan = invite.travel_plan
    travel_plan.users.add(invite.requested_by)
    invite.delete()
    return redirect('joinrequests')


def decline_invite(request):
    id = request.GET.get('id')
    invite = get_object_or_404(Invite, id=id)
    invite.delete()
    return redirect('joinrequests')


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

        # Add debug output
        travel_plan = self.object
        destinations = Destination.objects.filter(travel_plan=travel_plan)
        paginator = Paginator(destinations, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        if travel_plan.jpg_upload_file:
            metadata = travel_plan.jpg_metadata.all()
            print(f"Found {metadata.count()} metadata entries for travel plan {travel_plan.id}")
            if metadata:
                print(f"Metadata title: {metadata[0].file_title}")
                print(f"Metadata description: {metadata[0].description}")

        return context

    def get_object(self):
        group_code = self.kwargs.get("primary_group_code")
        return get_object_or_404(TravelPlan, primary_group_code=group_code)


class DestinationView(generic.DetailView):
    model = Destination
    template_name = "users/destination_detail.html"
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        id = self.kwargs["id"]
        context = {}
        context['destination'] = Destination.objects.filter(travel_plan=self.object, id=id).first()
        context['form'] = CommentForm()
        # print(destination.destination_name)
        travelplan = context['destination'].travel_plan
        # Add debug output
        # travel_plan = self.object
        # destinations = Destination.objects.filter(travel_plan=travel_plan)
        # paginator = Paginator(destinations, 2)
        # page_number = self.request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        context['travelplan'] = travelplan
        return context
        # context['page_obj'] = page_obj
        # if travel_plan.jpg_upload_file:
        #     metadata = travel_plan.jpg_metadata.all()
        #     print(f"Found {metadata.count()} metadata entries for travel plan {travel_plan.id}")
        #     if metadata:
        #         print(f"Metadata title: {metadata[0].file_title}")
        #         print(f"Metadata description: {metadata[0].description}")
        #
        # return context

    def post(self, request, *args, **kwargs):
        destination_id = kwargs.get("id")
        destination = Destination.objects.filter(travel_plan__primary_group_code=kwargs.get("primary_group_code"),
                                                 id=destination_id).first()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.destination = destination
            comment.save()
            return redirect('destination_detail', primary_group_code=destination.travel_plan.primary_group_code,
                            id=destination.id)

    def get_object(self):
        group_code = self.kwargs.get("primary_group_code")
        return get_object_or_404(TravelPlan, primary_group_code=group_code)
