from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import TravelPlan, GroupCode
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
        widgets = {
            'plan_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlInput1',
                'placeholder': ''
            }),
            'group_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'typeNumber',
                'min': 1,
                'max': 20
            }),
            'trip_description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': 3
            }),
            'jpg_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'jpg_upload_file',
                'accept': '.jpg'
            }),
            'txt_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'txt_upload_file',
                'accept': '.txt'
            }),
            'pdf_upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'pdf_upload_file',
                'accept': '.pdf'
            }),
        }

    def save(self, commit=True, user=None):
        travel_plan = super().save(commit=False)
        
        # Generate a unique group code
        unique_code = str(uuid.uuid4())[:8]  # Generate an 8-character unique code
        group_code, created = GroupCode.objects.get_or_create(code=unique_code)
        if user:
            group_code.users.add(user)
        travel_plan.primary_group_code = group_code

        if commit:
            travel_plan.save()
            self.save_m2m()  # Save many-to-many relationships
        return travel_plan