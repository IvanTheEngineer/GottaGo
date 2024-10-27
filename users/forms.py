from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from models import TravelPlan, Destination
import uuid


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class PlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = [
            'plan_name',
            'group_size',
            'trip_description',
            'jpg_upload_file',
            'txt_upload_file',
            'pdf_upload_file',
        ]
        labels = {
            'jpg_upload_file': 'Upload an image for the trip',
            'txt_upload_file': 'Upload a text file with trip details',
            'pdf_upload_file': 'Upload a PDF document',
        }
        widgets = {
            'plan_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlInput1',
                'placeholder': 'Enter your plan name'
            }),
            'group_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'typeNumber',
                'min': 1,
                'max': 20,
                'placeholder': 'Number of people'
            }),
            'trip_description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': 3,
                'placeholder': 'Details about the trip'
            }),
            'jpg_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'jpg_upload_file',
                'accept': '.jpg',
            }),
            'txt_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'txt_upload_file',
                'accept': '.txt',
            }),
            'pdf_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'pdf_upload_file',
                'accept': '.pdf',
            }),
        }

    def save(self, commit=True, user=None):
        travel_plan = super().save(commit=False)

        # Generate a unique group code
        unique_code = str(uuid.uuid4())[:8]  # Generate an 8-character unique code
        travel_plan.primary_group_code = unique_code

        if user is not None:
            travel_plan.user = user  # Set the user field

        travel_plan.save()

        if user is not None:
            travel_plan.users.add(user)  # Add the user to the many-to-many relationship

        return travel_plan


class DestinationForm(forms.Form):
    class Meta:
        model = Destination
        fields = [
            'destination_name',
            'destination_description',
            'jpg_upload_file',
            'txt_upload_file',
            'pdf_upload_file',
        ]
        labels = {
            'jpg_upload_file': 'Upload an image for the destination',
            'txt_upload_file': 'Upload a text file with destination details',
            'pdf_upload_file': 'Upload a PDF document',
        }
        widgets = {
            'destination_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlInput1',
                'placeholder': 'Enter your destination name'
            }),
            'destination_description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': 3,
                'placeholder': 'Details about the destination'
            }),
            'jpg_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'jpg_upload_file',
                'accept': '.jpg',
            }),
            'txt_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'txt_upload_file',
                'accept': '.txt',
            }),
            'pdf_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'pdf_upload_file',
                'accept': '.pdf',
            }),
        }

    def save(self, commit=True, travel_plan=None):
        destination = super().save(commit=False)

        # if user is not None:
        #     destination.user = user  # Set the user field

        # Todo: Set the travel_plan

        if travel_plan is not None:
            destination.travel_plan = travel_plan

        # if user is not None:
        #     destination.users.add(user)  # Add the user to the many-to-many relationship

        return destination


class JoinGroupForm(forms.Form):
    group_code = forms.CharField(max_length=64, label='Group Code')
