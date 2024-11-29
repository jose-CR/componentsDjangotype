from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.authentication.auth import Authentication

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    return Authentication.get_signup(request)

def signout(request):
    return Authentication.get_signout(request)

def signing(request):
    return Authentication.get_signing(request)

@login_required
def logged(request):
    return Authentication.get_logged(request)

def custom_dispatch(request, *args, **kwargs):
    return Authentication.dispatch(request, *args, **kwargs)