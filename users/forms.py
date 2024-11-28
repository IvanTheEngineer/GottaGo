from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import TravelPlan, Destination, FileMetadata, Comment, Expense
import uuid
from django.core.validators import MinValueValidator

class DateInput(forms.DateInput):
    input_type = 'date'

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
    start_date = forms.DateField(widget=DateInput(attrs={'id': 'start_date'}))
    end_date = forms.DateField(widget=DateInput(attrs={'id': 'end_date'}))

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
            'start_date',
            'end_date',
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
            'start_date': 'Enter Start Date',
            'end_date': 'Enter End Date',
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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "End date must be greater than or equal to the start date.")

        return cleaned_data

    def save(self, commit=True, user=None):
        travel_plan = super().save(commit=False)

        # Generate a unique group code
        if not travel_plan.primary_group_code:
            unique_code = str(uuid.uuid4())[:8]  # Generate an 8-character unique code
            travel_plan.primary_group_code = unique_code

        if user is not None:
            travel_plan.user = user  # Set the user field

        travel_plan.save()

        if user is not None:
            travel_plan.users.add(user)

        if travel_plan.jpg_upload_file:
        # Update or create metadata
            if travel_plan.jpg_metadata:
                if (self.cleaned_data.get('jpg_file_title') == "" and self.cleaned_data.get('jpg_description') == "" and self.cleaned_data.get('jpg_keywords') == ""):
                    travel_plan.jpg_metadata.delete()
                    travel_plan.jpg_metadata = None
                else: 
                    travel_plan.jpg_metadata.file_title = self.cleaned_data.get('jpg_file_title', '')
                    travel_plan.jpg_metadata.description = self.cleaned_data.get('jpg_description', '')
                    travel_plan.jpg_metadata.keywords = self.cleaned_data.get('jpg_keywords', '')
                    travel_plan.jpg_metadata.save()
            elif not (self.cleaned_data.get('jpg_file_title') == "" and self.cleaned_data.get('jpg_description') == "" and self.cleaned_data.get('jpg_keywords') == ""):
                jpg_metadata = FileMetadata.objects.create(
                    content_object=travel_plan,
                    file_title=self.cleaned_data.get('jpg_file_title', ''),
                    description=self.cleaned_data.get('jpg_description', ''),
                    keywords=self.cleaned_data.get('jpg_keywords', '')
                )
                travel_plan.jpg_metadata = jpg_metadata
                travel_plan.save() 
        elif travel_plan.jpg_metadata:
            # Delete metadata if file is removed
            travel_plan.jpg_metadata.delete()
            travel_plan.jpg_metadata = None

        if travel_plan.txt_upload_file:
        # Update or create metadata
            if travel_plan.txt_metadata:
                if (self.cleaned_data.get('txt_file_title') == "" and self.cleaned_data.get('txt_description') == "" and self.cleaned_data.get('txt_keywords') == ""):
                    travel_plan.txt_metadata.delete()
                    travel_plan.txt_metadata = None
                else:
                    travel_plan.txt_metadata.file_title = self.cleaned_data.get('txt_file_title', '')
                    travel_plan.txt_metadata.description = self.cleaned_data.get('txt_description', '')
                    travel_plan.txt_metadata.keywords = self.cleaned_data.get('txt_keywords', '')
                    travel_plan.txt_metadata.save()
            elif not (self.cleaned_data.get('txt_file_title') == "" and self.cleaned_data.get('txt_description') == "" and self.cleaned_data.get('txt_keywords') == ""):
                txt_metadata = FileMetadata.objects.create(
                    content_object=travel_plan,
                    file_title=self.cleaned_data.get('txt_file_title', ''),
                    description=self.cleaned_data.get('txt_description', ''),
                    keywords=self.cleaned_data.get('txt_keywords', '')
                )
                travel_plan.txt_metadata = txt_metadata
                travel_plan.save() 
        elif travel_plan.txt_metadata:
            # Delete metadata if file is removed
            travel_plan.txt_metadata.delete()
            travel_plan.txt_metadata = None

        if travel_plan.pdf_upload_file:
        # Update or create metadata
            if travel_plan.pdf_metadata:
                if (self.cleaned_data.get('pdf_file_title') == "" and self.cleaned_data.get('pdf_description') == "" and self.cleaned_data.get('pdf_keywords') == ""):
                    travel_plan.pdf_metadata.delete()
                    travel_plan.pdf_metadata = None
                else:
                    travel_plan.pdf_metadata.file_title = self.cleaned_data.get('pdf_file_title', '')
                    travel_plan.pdf_metadata.description = self.cleaned_data.get('pdf_description', '')
                    travel_plan.pdf_metadata.keywords = self.cleaned_data.get('pdf_keywords', '')
                    travel_plan.pdf_metadata.save()
            elif not (self.cleaned_data.get('pdf_file_title') == "" and self.cleaned_data.get('pdf_description') == "" and self.cleaned_data.get('pdf_keywords') == ""):
                pdf_metadata = FileMetadata.objects.create(
                    content_object=travel_plan,
                    file_title=self.cleaned_data.get('pdf_file_title', ''),
                    description=self.cleaned_data.get('pdf_description', ''),
                    keywords=self.cleaned_data.get('pdf_keywords', '')
                )
                travel_plan.pdf_metadata = pdf_metadata
                travel_plan.save() 
        elif travel_plan.pdf_metadata:
            # Delete metadata if file is removed
            travel_plan.pdf_metadata.delete()
            travel_plan.pdf_metadata = None

        return travel_plan


class DestinationForm(forms.ModelForm):
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

    # Add metadata fields for each file type
    latitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )
    longitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )
    location_address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.HiddenInput()
    )
    location_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.HiddenInput()
    )

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
            'latitude',
            'longitude',
            'location_address',
            'location_name',
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
            destination.user = user

        # Save the destination first
        destination.save()

        if user is not None:
            destination.users.add(user)

        if destination.jpg_upload_file:
        # Update or create metadata
            if destination.jpg_metadata:
                if (self.cleaned_data.get('jpg_file_title') == "" and self.cleaned_data.get('jpg_description') == "" and self.cleaned_data.get('jpg_keywords') == ""):
                    destination.jpg_metadata.delete()
                    destination.jpg_metadata = None
                else: 
                    destination.jpg_metadata.file_title = self.cleaned_data.get('jpg_file_title', '')
                    destination.jpg_metadata.description = self.cleaned_data.get('jpg_description', '')
                    destination.jpg_metadata.keywords = self.cleaned_data.get('jpg_keywords', '')
                    destination.jpg_metadata.save()
            elif not (self.cleaned_data.get('jpg_file_title') == "" and self.cleaned_data.get('jpg_description') == "" and self.cleaned_data.get('jpg_keywords') == ""):
                jpg_metadata = FileMetadata.objects.create(
                    content_object=destination,
                    file_title=self.cleaned_data.get('jpg_file_title', ''),
                    description=self.cleaned_data.get('jpg_description', ''),
                    keywords=self.cleaned_data.get('jpg_keywords', '')
                )
                destination.jpg_metadata = jpg_metadata
                destination.save() 
        elif destination.jpg_metadata:
            # Delete metadata if file is removed
            destination.jpg_metadata.delete()
            destination.jpg_metadata = None

        if destination.txt_upload_file:
        # Update or create metadata
            if destination.txt_metadata:
                if (self.cleaned_data.get('txt_file_title') == "" and self.cleaned_data.get('txt_description') == "" and self.cleaned_data.get('txt_keywords') == ""):
                    destination.txt_metadata.delete()
                    destination.txt_metadata = None
                else:
                    destination.txt_metadata.file_title = self.cleaned_data.get('txt_file_title', '')
                    destination.txt_metadata.description = self.cleaned_data.get('txt_description', '')
                    destination.txt_metadata.keywords = self.cleaned_data.get('txt_keywords', '')
                    destination.txt_metadata.save()
            elif not (self.cleaned_data.get('txt_file_title') == "" and self.cleaned_data.get('txt_description') == "" and self.cleaned_data.get('txt_keywords') == ""):
                txt_metadata = FileMetadata.objects.create(
                    content_object=destination,
                    file_title=self.cleaned_data.get('txt_file_title', ''),
                    description=self.cleaned_data.get('txt_description', ''),
                    keywords=self.cleaned_data.get('txt_keywords', '')
                )
                destination.txt_metadata = txt_metadata
                destination.save() 
        elif destination.txt_metadata:
            destination.txt_metadata.delete()
            destination.txt_metadata = None

        if destination.pdf_upload_file:
        # Update or create metadata
            if destination.pdf_metadata:
                if (self.cleaned_data.get('pdf_file_title') == "" and self.cleaned_data.get('pdf_description') == "" and self.cleaned_data.get('pdf_keywords') == ""):
                    destination.pdf_metadata.delete()
                    destination.pdf_metadata = None
                else:
                    destination.pdf_metadata.file_title = self.cleaned_data.get('pdf_file_title', '')
                    destination.pdf_metadata.description = self.cleaned_data.get('pdf_description', '')
                    destination.pdf_metadata.keywords = self.cleaned_data.get('pdf_keywords', '')
                    destination.pdf_metadata.save()
            elif not (self.cleaned_data.get('pdf_file_title') == "" and self.cleaned_data.get('pdf_description') == "" and self.cleaned_data.get('pdf_keywords') == ""):
                pdf_metadata = FileMetadata.objects.create(
                    content_object=destination,
                    file_title=self.cleaned_data.get('pdf_file_title', ''),
                    description=self.cleaned_data.get('pdf_description', ''),
                    keywords=self.cleaned_data.get('pdf_keywords', '')
                )
                destination.pdf_metadata = pdf_metadata
                destination.save() 
        elif destination.pdf_metadata:
            # Delete metadata if file is removed
            destination.pdf_metadata.delete()
            destination.pdf_metadata = None

        return destination


class JoinGroupForm(forms.Form):
    group_code = forms.CharField(max_length=64, label='Group Code')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentText']
        widgets = {
            'commentText': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment!'
            })
        }


class ExpenseForm(forms.ModelForm):
    """Form for creating and editing expenses"""
    class Meta:
        model = Expense
        fields = ['expense_name', 'amount', 'expense_date']
        widgets = {
            'expense_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter expense name'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'min': '0',
                'step': '0.01'
            }),
            'expense_date': DateInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'expense_name': 'Expense Name',
            'amount': 'Amount ($)',
            'expense_date': 'Date'
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("Amount cannot be negative")
        return amount
