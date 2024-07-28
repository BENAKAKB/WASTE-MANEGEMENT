
from django.db import IntegrityError

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, ReportIssueForm, RequestPickupForm,AddImageForm, UpdateIssueForm
from .models import WasteIssue, PickupRequest
from django.http import HttpRequest
def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"Attempting to authenticate user: {email}") 
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                print("Authentication failed")  
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data["user_role"] == 'admin':
                user.is_staff = True
                user.save()
            auth_login(request, user)  
            return redirect('user_dashboard' if user.is_staff else 'user_dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def report_issue(request):
    if request.method == 'POST':
        form = ReportIssueForm(request.POST)
        if form.is_valid():
            try:
                pickup = form.save(commit=False)
                pickup.requested_by = request.user
                pickup.save()
                return redirect('user_dashboard')
            except IntegrityError as e:
                form.add_error(None, "An error occurred: Foreign key constraint failed.")
                print(f"IntegrityError: {e}")
    else:
        form = ReportIssueForm()
    return render(request, 'user/report_issue.html', {'form': form})

@login_required
def request_pickup(request):
    if request.method == 'POST':
        form = RequestPickupForm(request.POST)
        if form.is_valid():
            try:
                pickup = form.save(commit=False)
                pickup.requested_by = request.user
                pickup.save()
                return redirect('user_dashboard')
            except IntegrityError as e:
                form.add_error(None, "An error occurred: Foreign key constraint failed.")
                print(f"IntegrityError: {e}")
    else:
        form = RequestPickupForm()
    return render(request, 'user/request_pickup.html', {'form': form})

@login_required
def user_dashboard(request):
    user = request.user
    issues = WasteIssue.objects.filter(reported_by=user)
    pickups = PickupRequest.objects.filter(requested_by=user)
    return render(request, 'user/user_dashboard.html', {'issues': issues, 'pickups': pickups})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')  
    issues = WasteIssue.objects.all()
    pickups = PickupRequest.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'issues': issues, 'pickups': pickups})

@login_required
def admin_update_issue(request, issue_id):
    if not request.user.is_staff:
        return redirect('login')

    issue = get_object_or_404(WasteIssue, id=issue_id)

    if request.method == 'POST':
        form = UpdateIssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()  # Save the form data, which updates the issue instance
            return redirect('admin_dashboard')  # Redirect to admin dashboard after successful update
    else:
        form = UpdateIssueForm(instance=issue)

    return render(request, 'admin/admin_update_issue.html', {'form': form, 'issue': issue})

@login_required
def admin_update_pickup(request, pickup_id):
    if not request.user.is_staff:
        return redirect('login')  
    pickup = PickupRequest.objects.get(id=pickup_id)
    if request.method == 'POST':
       
        return redirect('admin_dashboard')
    return render(request, 'admin/admin_update_pickup.html', {'pickup': pickup})
def add_image(request):
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = AddImageForm()
    return render(request, 'user/add_image.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')
