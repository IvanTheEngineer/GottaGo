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
from .forms import (
    PlanForm,
    JoinGroupForm,
    DestinationForm,
    CommentForm,
    ExpenseForm
)
from .decorators import user_not_authenticated
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import TravelPlan, Destination, Invite, Comment, Expense
from django.http import FileResponse, Http404
from django.http import JsonResponse
import requests
import boto3
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum


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
    error_message = ""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PlanForm(request.POST, request.FILES)
            if is_pma_admin(request.user):
                form.add_error(None, 'PMA administrators are not able to create a project.')
                error_message = "PMA administrators are not able to create a project."
            elif form.is_valid():
                plan = form.save(commit=False, user=request.user)
                print(request.user)
                plan.user = request.user
                plan.save()
                # print(f"File uploaded to S3: {plan.jpg_upload_file.url}")
                return redirect('plans')
        else:
            form = PlanForm()
        return render(request, 'users/project_creator.html', {'form': form, "error_message": error_message})
    else:
        return render(request, 'users/project_creator.html')


class TravelPlanUpdateView(generic.UpdateView):
    model = TravelPlan
    form_class = PlanForm
    template_name = 'users/project_editor.html'

    def dispatch(self, request, *args, **kwargs):
        travel_plan = self.get_object()
        if request.user not in travel_plan.users.all() and not is_pma_admin(request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        group_code = self.kwargs.get("primary_group_code")
        return get_object_or_404(TravelPlan, primary_group_code=group_code)

    def get_success_url(self):
        primary_group_code = self.object.primary_group_code
        return reverse_lazy('detail', kwargs={'primary_group_code': primary_group_code})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        travel_plan = self.get_object()
        context['form'].initial[
            'txt_file_title'] = travel_plan.txt_metadata.file_title if travel_plan.txt_metadata else ''
        context['form'].initial[
            'txt_description'] = travel_plan.txt_metadata.description if travel_plan.txt_metadata else ''
        context['form'].initial['txt_keywords'] = travel_plan.txt_metadata.keywords if travel_plan.txt_metadata else ''
        context['form'].initial[
            'pdf_file_title'] = travel_plan.pdf_metadata.file_title if travel_plan.pdf_metadata else ''
        context['form'].initial[
            'pdf_description'] = travel_plan.pdf_metadata.description if travel_plan.pdf_metadata else ''
        context['form'].initial['pdf_keywords'] = travel_plan.pdf_metadata.keywords if travel_plan.pdf_metadata else ''
        context['form'].initial[
            'jpg_file_title'] = travel_plan.jpg_metadata.file_title if travel_plan.jpg_metadata else ''
        context['form'].initial[
            'jpg_description'] = travel_plan.jpg_metadata.description if travel_plan.jpg_metadata else ''
        context['form'].initial['jpg_keywords'] = travel_plan.jpg_metadata.keywords if travel_plan.jpg_metadata else ''
        context['has_txt_metadata'] = bool(travel_plan.txt_metadata)
        context['has_pdf_metadata'] = bool(travel_plan.pdf_metadata)
        context['has_jpg_metadata'] = bool(travel_plan.jpg_metadata)

        context['primary_group_code'] = self.kwargs.get("primary_group_code")
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


# <a style="margin-bottom: 10px; margin-top: 10px;" href="{% url 'edit_destination' primary_group_code=destination.travel_plan.primary_group_code id=destination.id %}" class="btn btn-primary">Edit</a>
class DestinationUpdateView(generic.UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'users/destination_editor.html'

    def dispatch(self, request, *args, **kwargs):
        destination = self.get_object()
        if request.user not in destination.travel_plan.users.all() and not is_pma_admin(request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(Destination, id=id)

    def get_success_url(self):
        primary_group_code = self.object.travel_plan.primary_group_code
        return reverse_lazy('destination_detail',
                            kwargs={'primary_group_code': primary_group_code, 'id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the destination instance
        destination = self.get_object()

        # Pre-populate metadata for the form
        context['form'].initial[
            'txt_file_title'] = destination.txt_metadata.file_title if destination.txt_metadata else ''
        context['form'].initial[
            'txt_description'] = destination.txt_metadata.description if destination.txt_metadata else ''
        context['form'].initial['txt_keywords'] = destination.txt_metadata.keywords if destination.txt_metadata else ''
        context['form'].initial[
            'pdf_file_title'] = destination.pdf_metadata.file_title if destination.pdf_metadata else ''
        context['form'].initial[
            'pdf_description'] = destination.pdf_metadata.description if destination.pdf_metadata else ''
        context['form'].initial['pdf_keywords'] = destination.pdf_metadata.keywords if destination.pdf_metadata else ''
        context['form'].initial[
            'jpg_file_title'] = destination.jpg_metadata.file_title if destination.jpg_metadata else ''
        context['form'].initial[
            'jpg_description'] = destination.jpg_metadata.description if destination.jpg_metadata else ''
        context['form'].initial['jpg_keywords'] = destination.jpg_metadata.keywords if destination.jpg_metadata else ''
        context['has_txt_metadata'] = bool(destination.txt_metadata)
        context['has_pdf_metadata'] = bool(destination.pdf_metadata)
        context['has_jpg_metadata'] = bool(destination.jpg_metadata)

        context['location_name'] = destination.location_name if destination.location_name else ''
        context['location_address'] = destination.location_address if destination.location_address else ''
        context['latitude'] = destination.latitude if destination.latitude else ''
        context['longitude'] = destination.longitude if destination.longitude else ''

        context['primary_group_code'] = self.kwargs.get("primary_group_code")
        return context

    def get_initial(self):
        initial = super().get_initial()

        # Retrieve the destination and its metadata
        destination = self.get_object()

        # Populate metadata fields if they exist
        if destination.txt_metadata:
            initial['txt_file_title'] = destination.txt_metadata.file_title
            initial['txt_description'] = destination.txt_metadata.description
            initial['txt_keywords'] = destination.txt_metadata.keywords

        return initial


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


def delete_destination(request):
    id = request.GET.get('id')
    destination = get_object_or_404(Destination, id=id)
    destination.delete()
    messages.success(request, 'Successfully deleted the destination.')
    if is_pma_admin(request.user):
        return redirect('all_plans')
    return redirect('detail', destination.travel_plan.primary_group_code)


def all_plans_view(request):
    if not is_pma_admin(request.user):
        return redirect('plans')
    all_travel_plans = TravelPlan.objects.all().prefetch_related('users')
    print(f"Plans found: {all_travel_plans.count()}")
    context = {'all_travel_plans': all_travel_plans}
    return render(request, 'users/all_plans.html', context)


def explore_plans_view(request):
    explore_travel_plans = TravelPlan.objects.all()
    paginator = Paginator(explore_travel_plans, 4)
    page = request.GET.get('page')
    try:
        paginated_explore_plans = paginator.page(page)
    except PageNotAnInteger:
        paginated_explore_plans = paginator.page(1)
    except EmptyPage:
        paginated_explore_plans = paginator.page(paginator.num_pages)

    context = {'explore_travel_plans': paginated_explore_plans}
    # context = {'explore_travel_plans': explore_travel_plans}
    return render(request, 'users/explore_plans.html', context)


def user_plans_view(request):
    if request.user.is_authenticated:
        # Get all plans the user is in
        travel_plans = TravelPlan.objects.filter(Q(user=request.user) | Q(users=request.user)).distinct()
        destinations = Destination.objects.filter(travel_plan__in=travel_plans)

        # Add an explicit ordering to the queryset
        travel_plans = travel_plans.order_by('start_date')  # or any other field
        paginator = Paginator(travel_plans, 3)
        page = request.GET.get('page')
        try:
            paginated_travel_plans = paginator.page(page)
        except PageNotAnInteger:
            paginated_travel_plans = paginator.page(1)
        except EmptyPage:
            paginated_travel_plans = paginator.page(paginator.num_pages)

        for plan in travel_plans:
            print(plan.id)
        # return render(request, 'users/plans.html', {'travel_plans': travel_plans})

        return render(request, 'users/plans.html',
                      {'travel_plans': paginated_travel_plans, 'destinations': destinations})
        # return render(request, 'users/plans.html', {'travel_plans': travel_plans, 'destinations': destinations})

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
                except Http404:
                    context['error_message'] = 'Invalid group code. Please try again.'
        else:
            pass
        return render(request, 'users/join_group.html', context)
    else:
        return render(request, 'users/join_group.html')


def joinrequests(request):
    print(request.user)
    if request.user.is_authenticated:
        invites = Invite.objects.filter(requested_to=request.user)
        return render(request, 'users/requests.html', {'invites': invites})
    else:
        return render(request, 'users/requests.html')


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

    def dispatch(self, request, *args, **kwargs):
        travel_plan = self.get_object()
        if request.user not in travel_plan.users.all() and not is_pma_admin(request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destinations = Destination.objects.filter(travel_plan=self.object)
        context['destinations'] = destinations
        destination_data = [
            {
                "name": destination.location_name,
                "address": destination.location_address,
                "latitude": destination.latitude,
                "longitude": destination.longitude,
            }
            for destination in destinations if destination.latitude and destination.longitude
        ]
        context["destination_data"] = destination_data

        # Calculate total expenses for all destinations in this travel plan
        total_plan_expenses = Expense.objects.filter(
            destination__travel_plan=self.object
        ).aggregate(total=Sum('amount'))['total'] or 0
        context['total_plan_expenses'] = total_plan_expenses

        # Add debug output
        travel_plan = self.object
        destinations = Destination.objects.filter(travel_plan=travel_plan)
        paginator = Paginator(destinations, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context

    def get_object(self):
        group_code = self.kwargs.get("primary_group_code")
        return get_object_or_404(TravelPlan, primary_group_code=group_code)


class DestinationView(generic.DetailView):
    model = Destination
    template_name = "users/destination_detail.html"
    context_object_name = 'destination'

    def dispatch(self, request, *args, **kwargs):
        travel_plan = self.get_object()
        if request.user not in travel_plan.users.all() and not is_pma_admin(request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        id = self.kwargs["id"]
        context = {}
        destination = Destination.objects.filter(travel_plan=self.object, id=id).first()
        context['destination'] = destination
        context['form'] = CommentForm()
        travelplan = context['destination'].travel_plan
        context['travelplan'] = travelplan

        # Add total expenses calculation
        total_expenses = Expense.objects.filter(destination=context['destination']).aggregate(total=Sum('amount'))[
            'total']
        context['total_expenses'] = total_expenses

        comments = Comment.objects.filter(destination=context['destination'])
        paginator = Paginator(comments, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        if destination.latitude and destination.longitude:
            context['saved_location'] = {
                'lat': destination.latitude,
                'lng': destination.longitude,
                'name': destination.location_name,
                'address': destination.location_address,
            }
        else:
            context['saved_location'] = None
        return context

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


def destination_budget(request, primary_group_code, id):
    destination = get_object_or_404(Destination, id=id, travel_plan__primary_group_code=primary_group_code)
    travelplan = destination.travel_plan
    error_message = ""
    if request.user not in travelplan.users.all():
        return redirect('home')

    if request.method == 'POST' and request.user.is_authenticated:
        form = ExpenseForm(request.POST)
        if form.is_valid():
            if is_pma_admin(request.user):
                error_message = "PMA administrators are not able to add budget items."
            else:
                expense = form.save(commit=False)
                expense.destination = destination
                expense.created_by = request.user
                expense.save()
                messages.success(request, 'Expense added successfully!')
                return redirect('destination_budget', primary_group_code=primary_group_code, id=id)


    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(destination=destination).order_by('-expense_date')
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    formatted_total_amount = f"{total_amount:.2f}"

    context = {
        'destination': destination,
        'travelplan': travelplan,
        'expense_form': form,
        'expenses': expenses,
        'total_amount': formatted_total_amount,
        'error_message': error_message
    }

    return render(request, 'users/destination_budget.html', context)


@login_required
def delete_expense(request, primary_group_code, id, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    # Check if the user is authorized to delete this expense
    if request.user != expense.created_by:
        messages.error(request, 'You are not authorized to delete this expense.')
        return redirect('destination_budget',
                        primary_group_code=primary_group_code,
                        id=id)

    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('destination_budget',
                    primary_group_code=primary_group_code,
                    id=id)


def save_location(request, primary_group_code, id, destination_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            travel_plan = get_object_or_404(TravelPlan, primary_group_code=primary_group_code)
            destination = get_object_or_404(Destination, id=destination_id, travel_plan=travel_plan)

            destination.location_name = data.get('name')
            destination.location_address = data.get('address')
            destination.latitude = data.get('lat')
            destination.longitude = data.get('lng')
            destination.save()

            return JsonResponse({'success': True, 'message': 'Location saved successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
