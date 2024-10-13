

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import ServiceRequest
from .forms import ServiceRequestForm, UserRegistrationForm# consumer_services/views.py
from django.contrib import messages
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            messages.success(request, "Your service request has been submitted successfully!")
            return redirect('track_request')
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

@login_required
def track_request(request):
    requests = ServiceRequest.objects.filter(customer=request.user).order_by('-submitted_at')
    return render(request, 'track_request.html', {'requests': requests})

@login_required
def account_info(request):
    return render(request, 'account_info.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def manage_requests(request):
    # Ensure only staff members can access this view
    if not request.user.is_staff:
        return redirect('home')

    requests = ServiceRequest.objects.all().order_by('-submitted_at')
    return render(request, 'manage_requests.html', {'requests': requests})

@login_required
def update_request_status(request, request_id):
    # Ensure only staff members can access this view
    if not request.user.is_staff:
        return redirect('home')

    service_request = ServiceRequest.objects.get(id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        service_request.status = new_status
        if new_status == 'Completed':
            service_request.resolved_at = timezone.now()  # Set resolved_at to current time
        service_request.save()
        messages.success(request, f"Request status updated to {new_status}.")
        return redirect('manage_requests')

    return render(request, 'update_request.html', {'service_request': service_request})


def home(request):
    return render(request, 'home.html')

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('track_request')
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

@login_required
def track_request(request):
    requests = ServiceRequest.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'track_request.html', {'requests': requests})

@login_required
def account_info(request):
    return render(request, 'account_info.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})