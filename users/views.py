from logging.config import valid_ident
from typing import Protocol
from django.shortcuts import render, redirect
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


def home(request):
    user = request.user
    context = {
        'PMA': user.groups.filter(name='PMA').exists(),
    }
    return render(request, 'users/home.html', context)
