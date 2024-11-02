from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import TravelPlan, Destination, FileMetadata
import uuid


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class FileMetadataForm(forms.ModelForm):
    """Form for handling file metadata"""
    class Meta:
        model = FileMetadata
        fields = ['file_title', 'description', 'keywords']
        widgets = {
            'file_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title for this file'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the contents of this file'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter keywords separated by commas'
            })
        }


class PlanForm(forms.ModelForm):
    jpg_file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title for the image'
        })
    )
    jpg_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Describe the image contents'
        })
    )
    jpg_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
    )

    pdf_file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title for the PDF'
        })
    )
    pdf_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Describe the PDF contents'
        })
    )
    pdf_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
    )
    txt_file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title for the text file'
        })
    )
    txt_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Describe the text file contents'
        })
    )
    txt_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
    )

    class Meta:
        model = TravelPlan
        fields = [
            'plan_name',
            'group_size',
            'trip_description',
            'jpg_upload_file',
            'jpg_file_title',
            'jpg_description',
            'jpg_keywords',
            'txt_upload_file',
            'txt_file_title',
            'txt_description',
            'txt_keywords',
            'pdf_upload_file',
            'pdf_file_title',
            'pdf_description',
            'pdf_keywords',
        ]
        labels = {
            'plan_name': 'Plan Name',
            'group_size': 'Group Size',
            'trip_description': 'Trip Description',
            'jpg_upload_file': 'Upload an image for the trip',
            'jpg_file_title': 'Image Title',
            'jpg_description': 'Image Description',
            'jpg_keywords': 'Image Keywords (comma-separated)',
            'txt_upload_file': 'Upload a text file with trip details',
            'txt_file_title': 'Text File Title',
            'txt_description': 'Text File Description',
            'txt_keywords': 'Text File Keywords (comma-separated)',
            'pdf_upload_file': 'Upload a PDF document',
            'pdf_file_title': 'PDF Title',
            'pdf_description': 'PDF Description',
            'pdf_keywords': 'PDF Keywords (comma-separated)',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set custom labels for metadata fields
        self.fields['jpg_file_title'].label = "Image Title"
        self.fields['jpg_description'].label = "Image Description"
        self.fields['jpg_keywords'].label = "Image Keywords (comma-separated)"
        
        self.fields['pdf_file_title'].label = "PDF Title"
        self.fields['pdf_description'].label = "PDF Description"
        self.fields['pdf_keywords'].label = "PDF Keywords (comma-separated)"
        
        self.fields['txt_file_title'].label = "Text File Title"
        self.fields['txt_description'].label = "Text File Description"
        self.fields['txt_keywords'].label = "Text File Keywords (comma-separated)"

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

        if commit:
            travel_plan.save()
            
            # Save metadata for each uploaded file
            if travel_plan.jpg_upload_file:
                FileMetadata.objects.create(
                    content_object=travel_plan,
                    file_title=self.cleaned_data['jpg_file_title'],
                    description=self.cleaned_data['jpg_description'],
                    keywords=self.cleaned_data['jpg_keywords']
                )
            
            if travel_plan.txt_upload_file:
                FileMetadata.objects.create(
                    content_object=travel_plan,
                    file_title=self.cleaned_data['txt_file_title'],
                    description=self.cleaned_data['txt_description'],
                    keywords=self.cleaned_data['txt_keywords']
                )
                
            if travel_plan.pdf_upload_file:
                FileMetadata.objects.create(
                    content_object=travel_plan,
                    file_title=self.cleaned_data['pdf_file_title'],
                    description=self.cleaned_data['pdf_description'],
                    keywords=self.cleaned_data['pdf_keywords']
                )

        return travel_plan


class DestinationForm(forms.ModelForm):
    # Add metadata fields for each file type
    jpg_file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title for the image'
        })
    )
    jpg_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Describe the image contents'
        })
    )
    jpg_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
    )

    txt_file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title for the text file'
        })
    )
    txt_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Describe the text file contents'
        })
    )
    txt_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
    )

    pdf_file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title for the PDF'
        })
    )
    pdf_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Describe the PDF contents'
        })
    )
    pdf_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
    )

    class Meta:
        model = Destination
        fields = [
            'destination_name',
            'destination_description',
            'jpg_upload_file',
            'jpg_file_title',
            'jpg_description',
            'jpg_keywords',
            'txt_upload_file',
            'txt_file_title',
            'txt_description',
            'txt_keywords',
            'pdf_upload_file',
            'pdf_file_title',
            'pdf_description',
            'pdf_keywords',
        ]
        labels = {
            'jpg_upload_file': 'Upload an image for the destination',
            'txt_upload_file': 'Upload a text file with destination details',
            'pdf_upload_file': 'Upload a PDF document',
        }
        widgets = {
            'destination_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your destination name'
            }),
            'destination_description': forms.Textarea(attrs={
                'class': 'form-control',
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

    def save(self, commit=True, travel_plan=None, user=None):
        destination = super().save(commit=False)

        if travel_plan is not None:
            destination.travel_plan = travel_plan
        if user is not None:
            destination.user = user  # Set the user field

        # Todo: Set the travel_plan

        destination.save()

        if user is not None:
            destination.users.add(user)

        if commit:
            destination.save()
            
            # Save metadata for each uploaded file
            if destination.jpg_upload_file:
                FileMetadata.objects.create(
                    content_object=destination,
                    file_title=self.cleaned_data['jpg_file_title'],
                    description=self.cleaned_data['jpg_description'],
                    keywords=self.cleaned_data['jpg_keywords']
                )
            
            if destination.txt_upload_file:
                FileMetadata.objects.create(
                    content_object=destination,
                    file_title=self.cleaned_data['txt_file_title'],
                    description=self.cleaned_data['txt_description'],
                    keywords=self.cleaned_data['txt_keywords']
                )
                
            if destination.pdf_upload_file:
                FileMetadata.objects.create(
                    content_object=destination,
                    file_title=self.cleaned_data['pdf_file_title'],
                    description=self.cleaned_data['pdf_description'],
                    keywords=self.cleaned_data['pdf_keywords']
                )

        return destination


class JoinGroupForm(forms.Form):
    group_code = forms.CharField(max_length=64, label='Group Code')
